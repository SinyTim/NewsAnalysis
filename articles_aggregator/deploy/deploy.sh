
# git clone https://github.com/SinyTim/NewsAnalysis.git

cd $HOME/NewsAnalysis/articles_aggregator
pip install -r requirements.txt

cd $HOME/NewsAnalysis/articles_aggregator/packages
source build.sh

export DAGSTER_HOME=$HOME/NewsAnalysis/articles_aggregator/dagster_home
cd $DAGSTER_HOME
nohup $HOME/.local/bin/dagster-daemon run &
nohup $HOME/.local/bin/dagit -h 0.0.0.0 -p 3000 &
