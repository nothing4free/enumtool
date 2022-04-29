# enumtool: an automatic asse enumeration script.
enumtool is an asset enumeration script that can detect a wide range of domains given an ASN or obtain a wide list of subdomains given a domain name. I plan on extending its functionality even further, but for now this is a tool I made that suits my needs for the Ethical Hacking subject in my Software Engineering studies.

## Use

First, install the required packages using ```pip install -r requirements.txt```.<br>
Once that's done, you can invoke the script using:

```python3 enumtool.py [-h] [-a AUTONOMOUS_SYSTEM] [-d DOMAIN] [-f FILE] -m MODE```

The available modes (as of now) are the following:
* **get_domains**: gets domains found in a given autonomous system (using this mode requires the flags -a, --as and -f, --file)
* **get_subdomains**: gets subdomains from a given domain name (using this mode requires the flag -d, --domain; -f, --file is optional)

## License
This project is licensed under the [WTFPL (Do What The Fuck You Want To License)](http://www.wtfpl.net/). You can use it, modify it and distribute it as you want although I would really appreciate a shoutout somewhere :)<br>
Have fun, friends!
