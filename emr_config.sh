wget https://repo.continuum.io/archive/Anaconda2-5.3.0-Linux-x86_64.sh -O ~/anaconda.sh
bash ~/anaconda.sh -b -p $HOME/anaconda
echo -e '\nexport PATH=$HOME/anaconda/bin:$PATH' >> $HOME/.bashrc && source $HOME/.bashrc

conda install -y pyspark
conda install -y boto3
pip install konlpy
