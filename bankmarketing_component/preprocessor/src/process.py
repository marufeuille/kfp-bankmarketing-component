import argparse
import logging
import oss2
import pandas as pd
import numpy as np

def main(argv=None):
    # 引数を解析
    parser = argparse.ArgumentParser(description='Preprocessor')
    parser.add_argument('--filename', type=str, help='Input file path on Aliyun ObjectStorage', required=True)
    parser.add_argument('--output', type=str, help='Output file dir path on Aliyun ObjectStorage', required=True)
    parser.add_argument('--accesskey', type=str, help='Aliyun AccessKey', required=True)
    parser.add_argument('--accesskeysecret', type=str, help='Aliyun AccessKeySecret', required=True)
    parser.add_argument('--endpoint', type=str, help='Aliyun OSS Endpoint', required=True)
    parser.add_argument('--bucketname', type=str, help='Aliyun OSS bucket name', required=True)
    args = parser.parse_args()

    # 表示するLogLevelの指定
    logging.getLogger().setLevel(logging.INFO)

    # OSSからデータの取得
    auth = oss2.Auth(args.accesskey, args.accesskeysecret)
    logging.info('Pulling file...')
    bucket = oss2.Bucket(auth, args.endpoint, args.bucketname)
    bucket.get_object_to_file(args.filename, '/tmp/input.csv')
    logging.info('Pulling file completed.')

    logging.info('Process file...')
    # ; -> ,
    with open('/tmp/input.csv') as f:
        contents = f.read().replace(";", ",")
        with open('/tmp/replaced.csv', 'w') as f2:
            f2.write(contents)
    df = pd.read_csv('/tmp/replaced.csv')

    # ダミー化
    df_r = pd.get_dummies(df, columns=[
            "job","marital","education","default",
            "housing","loan","contact", "month",
            "poutcome"
        ],
        drop_first=True
    )
    df_r = df_r.replace({'y': {"no": 0, "yes": 1}})

    # 分割
    np.random.seed(10)
    idx = np.random.randint(0, 10, (df_r.shape[0]))
    df_r[idx < 8].to_csv("/tmp/train.csv")
    df_r[idx >= 8].to_csv("/tmp/test.csv")
    
    # アップロード
    logging.info('Pushing file...')
    bucket.put_object_from_file(args.output + 'train.csv', '/tmp/train.csv')
    bucket.put_object_from_file(args.output + 'test.csv', '/tmp/test.csv')
    logging.info('Pushing file completed.')

if __name__== "__main__":
  main()