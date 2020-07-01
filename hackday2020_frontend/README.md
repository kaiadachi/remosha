# hackday_2020

## Frontend

```bash
# install dependencies
$ npm install

# serve with hot reload at localhost:3000
$ npm run dev

```

## backend

```bash
# install dependencies
$ pip install -r requirements.txt or pip3 install -r requirements.txt
めんどかったので、pipenvとかvenvとかは使ってないです。python書く人からするとキモいと思うので好きなの入れてもらえればm
僕も気が向いたら入れます。 

# serve with hot reload at localhost:9000
ホットリロード
$ python or python3 main.py
3000番にアクセスしてwebでSaveボタンを押すと、9000番にpostして/imagesに保存されます。

```

## https化

カメラの接続が、httpsではないと有効化されないので、下記の設定で実行できるようにする。

mkcertをインストール
```
$ brew install mkcert
```

localCAを作成
```
$ mkcert -install
```

証明書作成
```
$ mkcert localhost
```

鍵を移動
```
$ mkdir server
$ mv *.pem server
```

## 本番デプロイ

GCP上のVMインスタンスで稼働させます。

### 初期設定

gcloudの設定を行い、以下のコマンドを実行するとVMインスタンスにsshできます。
```
$ gcloud beta compute ssh --zone "asia-northeast1-b" "hackday2020" --project "hackday2020"
```

サーバー上でgithubの鍵の設定を行います。

鍵の設定
```
# 鍵作成
$ ssh-keygen -t rsa -C "xxxx@gmail.com"

# 公開鍵をgithubに登録
# https://github.com/settings/keys
$ cat .ssh/id_rsa.pub 
```

dockerとmakeをインストールする
```
$ sudo snap install docker
$ sudo apt install make
```

### デーモンを起動

単にmakeコマンドを実行すると、
- cleanコンテナを削除
- コンテナのビルド
- コンテナの起動
が実行されます

backend
```
$ git clone git@github.com:HackDay2020/hackday2020_backend.git
$ cd hackday2020_backend
$ make
```

frontend
```
$ git clone git@github.com:HackDay2020/hackday2020_frontend.git
$ cd hackday2020_front
$ make
```

ログを見るには、Makefileのあるディレクトリで下記を実行してください。

```
$ make log
```

## 公開先
TODO: https化, ドメインの設定

* http://34.84.177.20
