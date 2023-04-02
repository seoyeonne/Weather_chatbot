from flask import Flask, request
from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib import parse
import datetime
import requests

app = Flask(__name__)


@app.route('/')  # this is the home page route
def hello_world(
):  # this is the home page function that generates the page code
  return "Hello world! This is WeatherBot"


@app.route('/webhook', methods=['POST'])
def webhook():
  req = request.get_json(silent=True, force=True)
  fulfillmentText = ''
  sum = 0
  query_result = req.get('queryResult')

  if query_result.get('action') == 'add.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    sum = str(num1 + num2)
    print('here num1 = {0}'.format(num1))
    print('here num2 = {0}'.format(num2))
    fulfillmentText = 'The sum of the two numbers is ' + sum

  elif query_result.get('action') == 'multiply.numbers':
    num1 = int(query_result.get('parameters').get('number'))
    num2 = int(query_result.get('parameters').get('number1'))
    product = str(num1 * num2)
    print('here num1 = {0}'.format(num1))
    print('here num2 = {0}'.format(num2))
    fulfillmentText = 'The multifly of the two numbers is ' + product

  elif query_result.get('action') == 'get.Holiday':
    print('get.Restday')
    year = 2023
    serviceKey = "zTFSo2OA2jMcSh4tr826KfhRa3ZguZZyVEGq%2BOZvLLqB6SSn0M3pUQf6bob7mUwSKPPDyyoiUdHDxVNK4OHUFg%3D%3D"
    product = '올해 공휴일 : '
    for month in range(3, 4):
      if month < 10:
        month = '0' + str(month)
      else:
        month = str(month)

      url = 'http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService'
      #공휴일 정보 조회
      operation = 'getRestDeInfo'
      params = {'solYear': year, 'solMonth': month}

      params = parse.urlencode(params)
      request_query = url + '/' + operation + '?' + params + '&' + 'serviceKey' + '=' + serviceKey
      get_data = requests.get(request_query)

      r = ['월', '화', '수', '목', '금', '토', '일']
      if True == get_data.ok:
        soup = BeautifulSoup(get_data.content, 'html.parser')
        item = soup.findAll('item')
        for i in item:
          day = int(i.locdate.string[-2:])
          aday = datetime.date(int(year), int(month), day)
          bday = aday.weekday()
          weekname = r[bday]
          temp_str = i.datename.string + i.isholiday.string + i.locdate.string + weekname
          product = product + '\n' + '*' + temp_str

    print(product)
    fulfillmentText = product

  elif query_result.get('action') == 'get.Weather':
    city = str(query_result.get('parameters').get('city'))
    when = str(query_result.get('parameters').get('when'))
    enc_city = parse.quote(city + '+날씨')
    url = 'https://search.naver.com/search.naver?ie=utf8&query=' + enc_city
    html = urlopen(url)
    bsObject = BeautifulSoup(html, "html.parser")

    if when == '내일':
      temp = bsObject.find('div', class_='weather_info type_tomorrow').find(
        'div', class_='temperature_text').text
      temp2 = bsObject.find('div', class_='weather_info type_tomorrow').find(
        'div', class_='temperature_info').text
      print('내일 ' + city + ' 날씨:: ' + temp + '도 입니다.')

    if when == '오늘':
      temp = bsObject.find('div', 'temperature_text').text
      temp2 = bsObject.find('p', 'summary').text
      print('오늘 ' + city + ' 날씨:: ' + temp + '도 입니다.')

    ans = '[알림] ' + when + ' ' + city + ':: ' + temp + '도 입니다.'
    product = ans + temp2
    fulfillmentText = product

  else:
    print("Fail")
  return {"fulfillmentText": fulfillmentText, "source": "webhookdata"}


if __name__ == '__main__':
  app.run(host='0.0.0.0',
          port=8080)  # This line is required to run Flask on repl.it
