
git clone https://github.com/SinyTim/NewsAnalysis.git
pip install -r requirements.txt
export DAGSTER_HOME=$HOME/NewsAnalysis/articles_aggregator/dagster_home
$HOME/.local/bin/dagster-daemon run
$HOME/.local/bin/dagit -h 0.0.0.0 -p 3000
