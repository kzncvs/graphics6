Deploying:

`$ sudo apt-get -y update`

`$ sudo apt-get -y install python3 python3-venv`

`$ git clone https://github.com/kzncvs/graphics6.git`

`$ cd graphics6`

`$ python3 -m venv venv`

`$ source venv/bin/activate`

`(venv) $ pip install -r requirements.txt`

Script launching:

`(venv) $ python3 main.py -tga <link to .tga file> -obj <link to .obj file>`
