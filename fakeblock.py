from flask import Flask, escape, request
from detect import check_if_fake

app = Flask("FakeBlock")

@app.route('/detect', methods=['POST'])
def detect():
    url = 'bruh'
    url = request.form.get('data')
    
    print(url)
    return check_if_fake(url)
        # print(check_if_fake(url))
    # return check_if_fake(url)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')