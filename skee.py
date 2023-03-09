from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from collections import defaultdict

# CHANGE THESE. Enter the roller names you want to collect scores
# for. You'll also need to enter the exact match ids from the 
# score.brewskeeball.com site for each of your matches.
ROLLERS = ['Bug Byte', 'Jameskee', 'Citro Nella', 'Gnatty Lite']
MATCH_IDS = ['6e9cPSoyqmGaiaMk6', 'ZrgonZWFR9rcpNQx8',
'3yP3w9nA3vKwcGNoa', 'DEGM4QK3MtXzevuty', 'mP8BAAjBgMrZtXyNS',
'ivotiRQ3prfMHPCAz', 'TuLczMWbHPM6bXjtS', 'KxjhxPnYMuAoxjsG9',
'tvxoct8pQ4oBXjpMd', 'SksgGG3NzJZPiBqZR', 'FnuJ3JakhbiS5Ycjn',
'cXvn7jj3yD4W3gXTo', 'h99Pt2RZQLxTb6m7k', 'TnhjfkacLfrHeKrQj',
'2hcR4AN8XxRsdNWbx', 'xYDMwg6NZoP3emfNp', '8GckW9JSJdyrjLtCJ',
'NcKKpMXy7LHtnTk57']

class Skee:
  '''
  The scrape fn is the meat here, it goes to the skee website
  and gets each frame for each ROLLER above. It saves them to
  a file, which can be consumed in excel or something later.

  You'll need to install Selenum on your computer. After that you
  should be able to run with `python3 skee.py`. You can calculate
  the averages per frame using the method below. It's easier to 
  export the frames in something like Google Sheets and get the
  per roll averages yourself.
  '''

  def __init__(self):
    self.per_frame_sum = defaultdict(list)


  def get_filename(self, roller):
    return "_".join([word.lower() for word in roller.split(" ")]) + "_scores.txt"


  def save_score(self, roller, scores):
    filename = self.get_filename(roller)
    with open(filename, 'a') as f:
      f.write(scores + '\n')
    print(f'Saving score {scores} to {filename}')


  def extract_score(self, line):
    period_pos = line.rfind('.')
    scores = line[period_pos+1:].strip()
    for roller in ROLLERS:
      if roller in line:
        self.save_score(roller, scores)


  def calculate_per_frame_avg(self):
    for input in [self.get_filename(roller) for roller in ROLLERS]:
      print(f'Averages for {input}')
      with open(input, 'r') as f:
        count = 0
        for line in f:
          rolls = [int(x.strip()) for x in line.split(',')]
          frame_sum = sum(rolls)
          self.per_frame_sum[count].append(frame_sum)
          count = (count + 1) % 10

      for k,v in self.per_frame_sum.items():
        avg = round(sum(v) / len(v), 2)
        print(f'FRAME {k+1}: {avg}')

      self.per_frame_sum = defaultdict(list)


  def scrape(self):
    driver = webdriver.Firefox()

    for match_id in MATCH_IDS:
      driver.get(f'https://score.brewskeeball.com/game/{match_id}/fullGameLog')
      wait = WebDriverWait(driver, 10)
      element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.list-group')))
      items = driver.find_elements(By.CSS_SELECTOR, 'div.list-group-item')

      for item in items:
        if 'rolled' in item.text:
          self.extract_score(item.text)

    driver.close()


if __name__ == '__main__':
  s = Skee()
  s.scrape()
  s.calculate_per_frame_avg()