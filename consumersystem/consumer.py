import time
import pika
import sys
import ast

from client import sendSMS, sendMail


class PushConsumer:
    def __init__(self, queue, exchange):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.queue = queue
        self.exchange = exchange
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.exchange_declare(exchange)
        self.channel.queue_bind(
            exchange=exchange,
            queue=queue,
        )

    def callback(self, ch, method, properties, body):
        # print(body)
        raw_body = eval(body)
        body_j = raw_body["data"]
        # print(body_j)
        if raw_body["type"] == "transaction":
            sendSMS(
                f"{body_j['sender_rmn']}",
                f"""
                Dear BankBuddy User,Your A/c XXX{body_j['sender_account']}-debited with amount of Rs.{body_j['amount']} on {body_j['date']} to XXX{body_j['reciever_account']}Ref No{body_j['txid']}
                """,
            )
        elif raw_body["type"] == "periodicbalance":
            raw_body = eval(body)
            body_j = raw_body["data"]
            sendSMS(
                f"{body_j['rmn']}",
                f"""
                Dear BankBuddy User,This is a monthly report on Your A/c XXX{body_j['account_number']}. Your balance is {body_j['balance']}" YOur account Status{body_j['status']}
                """,
            )

    def work(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=True
        )
        self.channel.start_consuming()


class PullConsumer:
    def __init__(self, queue, exchange):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        self.queue = queue
        self.exchange = exchange
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=queue)
        self.channel.exchange_declare(exchange)
        self.channel.queue_bind(
            exchange=exchange,
            queue=queue,
        )

    def callback(self, ch, method, properties, body):
        # print(body)
        raw_body = eval(body)
        body_j = raw_body["data"]
        # print(body_j)
        transaction_table = ""
        for i in body_j:
            transaction_table += f"{i['reciever']}  {i['amount']}  {i['time_stamp']}\n"
        if raw_body["type"] == "ministatement":
            sendMail(
                f"{raw_body['email']}",
                f"""
                Here Are your last 5 Transactions reciever amount Date \n
                {transaction_table}
                """,
            )

    def work(self):
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.callback, auto_ack=True
        )
        self.channel.start_consuming()
