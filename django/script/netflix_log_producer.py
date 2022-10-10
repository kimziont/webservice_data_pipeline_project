import json, time
from kafka import KafkaProducer

brokers = ["kafka:29092"]
for i in range(5):
    try:
        producer = KafkaProducer(bootstrap_servers = brokers)
        print(f'{i + 1}번 째 연결 성공')
        print(type(producer))
        break
    except:
        print(f'{i + 1}번 째 연결 실패')
else:
    print('Kafka를 연결할 수 없습니다')

topicName = "netflixWebLog"

# 프로듀서 시작할 때마다 웹 로그 파일에 기록된 로그 삭제 (어차피 이전에 카프카 토픽으로 보내졌으므로)
# 이렇게 하면 프로듀서를 시작할 때마다 토픽으로 중복 전송되는 것을 막을 수 있다
with open('/opt/netflix/logs/netflix.log', 'w') as f:
    f.write("\n")


with open('/opt/netflix/logs/netflix.log', 'r') as f:
    while True:
        row = f.readline()
        if row:
            producer.send(topicName, row.encode('utf-8'))
            print(row)
        time.sleep(0.1)