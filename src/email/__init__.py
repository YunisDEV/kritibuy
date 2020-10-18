from flask import Blueprint, request, make_response, render_template, url_for
import json
import requests
import sqlite3

def receipt_generator():
    html = render_template('receipt.html', data={
        "id": 15,
        "orderedTo": "Pragmatech",
        "orderedBy": "Yunis Huseynzade",
        "orderText": "I want to get web app from Pragmatech",
        "paid": True,
        "date": "2020-02-11 14:00:00"
    })
    return html


def send_email():
    x = receipt_generator()
    return x
