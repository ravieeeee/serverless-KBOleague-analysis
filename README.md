## Architecture

## Trouble Shooting
* serverless
  * lambda function 내 module을 import 못하는 에러
    * [serverless-python-requirements](https://github.com/UnitedIncome/serverless-python-requirements)로 해결
      * requirements.txt 내에 module들을 선언 -> 자동으로 환경 만들어줌
      * dockerize도 함(deploy시 local에 docker가 도는 상태여야 함)
    * 참고
      * [Serverless: Python - virtualenv - { "errorMessage": "Unable to import module 'handler'" }](https://markhneedham.com/blog/2017/08/06/serverless-python-virtualenv-errormessage-unable-import-module-handler/)
* EMR
  * 웹 연결 활성화(Amazon EMR 클러스터에 설치되는 애플리케이션은 마스터 노드에 호스팅된 웹 사이트로 사용자 인터페이스를 게시)를 위해 마스터 노드(EC2 인스턴스)에 대한 SSH 터널 열기 & 프록시 관리 도구 구성이 필요
    * EC2 key pair가 필요
    * 이 key pair는 EMR cluster 생성 시 필요하다
      * EC2 마스터 노드의 security rule에 22번 포트로 접근하는 ssh 액세스 허용 규칙이 없는 경우, [추가](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/authorizing-access-to-an-instance.html)
      * [Unprotected Private Key File Error](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/TroubleshootingInstancesConnecting.html#troubleshoot-unprotected-key)
    * [FoxyProxy](https://chrome.google.com/webstore/detail/foxyproxy-standard/gcknhkkoolaabfmlnjonogaaifnjlfnp?hl=ko) 설치 후, 관련 [설정](https://docs.aws.amazon.com/ko_kr/emr/latest/ManagementGuide/emr-connect-master-node-proxy.html#emr-connect-foxy-proxy-chrome)
  * Zeppelin에서 코드 실행시, –	java.net.ConnectException: Connection refused (Connection refused) 발생
    * Interpreter 설정이 제대로 안되어있는 문제(EC2에 당연히 Interpreter가 깔려있다고 생각했다)
      * [anaconda](https://www.anaconda.com/) 설치
        * 참고
          * [EC2 인스턴스에 anaconda 설치](https://hackernoon.com/aws-ec2-part-3-installing-anaconda-on-ec2-linux-ubuntu-dbef0835818a)
          * [Spark Cluster 구축하기](https://dziganto.github.io/amazon%20emr/apache%20spark/apache%20zeppelin/big%20data/From-Zero-to-Spark-Cluster-in-Under-Ten-Minutes/)
        * 과정
          * wget https://repo.continuum.io/archive/Anaconda2-5.3.0-Linux-x86_64.sh -O ~/anaconda.sh
          * bash ~/anaconda.sh -b -p $HOME/anaconda
          * echo -e '\nexport PATH=$HOME/anaconda/bin:$PATH' >> $HOME/.bashrc && source $HOME/.bashrc
  *	ec2 인스턴스 ssh 접속시 간헐적으로 connection이 매우 느린 현상

## Retrospect
* 크롤링 결과를 dynamodb에 넣은 것
  * dynamo는 Availability를 보장하는데, 이 프로젝트에는 그런 real-time을 보장받기 보다는 S3를 쓰는 것이 더 효율적이었을 것이다.
  *  [AWS Glue와 S3를 이용한 아키텍쳐 사례](https://aws.amazon.com/blogs/big-data/build-a-data-lake-foundation-with-aws-glue-and-amazon-s3/)
  * 이외에도 보통 이런 목적에는 S3를 많이 쓰는 사례를 많이 찾아볼 수 있다.
* serverless 배포시 python 가상 환경
  * 프로젝트용 가상 환경을 만들지 않았더니 requirements.txt 내에 local의 모든 파이썬 패키지가 들어감
