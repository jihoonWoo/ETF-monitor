from apscheduler.schedulers.blocking import BlockingScheduler
from etf_crawling import *

def exec_cron():
    RECORD_FILE = 'records/daily_records.csv'
    #crawl from betaShares
    betashares = {}
    betashares['Tech Savvy'] = 'nasdaq-100-etf'
    betashares['Sustainability Leaders'] = 'global-sustainability-leaders-etf'
    #crawl from iShares
    ishares = {}
    ishares['Aussie Top 200'] = '251852/ishares-core-s-and-p-asx-200-etf'
    ishares['Global 100'] = '273428/ishares-global-100-etf'
    ishares['Emerging Markets'] = '273417/ishares-msci-emerging-markets-etf'
    ishares['Health Wise'] = '273430/ishares-global-healthcare-etf'
    
    etf_crawling(RECORD_FILE, betashares, ishares)


def main():

    sched = BlockingScheduler(timezone="Australia/Melbourne")
    # excute program every Monday to Friday at 10:30am
    sched.add_job(exec_cron, trigger='cron', day_of_week='mon-fri', hour=11, minute=1)
    sched.start()


if __name__ == "__main__":
    main()