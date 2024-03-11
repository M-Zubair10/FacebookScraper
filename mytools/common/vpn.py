import random
import socket
import subprocess
import requests
import time


def check_ip(ipv4, api_key="38l350-798295-2034ji-sj2xj1"):
    """
    Using proxycheck.io to check ip as proxy or not
    :param ipv4: ip to be checked
    :param api_key: api_key of proxycheck.io
    :return: True if ip is clean i.e not proxy or vpn type else False
    """
    api_url = f"http://proxycheck.io/v2/{ipv4}?key={api_key}&vpn=1&asn=1&risk=1&port=1&seen=1&days=7&tag=msg"
    response = requests.get(api_url).json()
    return True if response[ipv4]['proxy'] == 'no' else False


class Mullvad:
    def __init__(self, timeout=10):
        self.country = None
        self.timeout = timeout
        self.socks = ['au3-wg.socks5.mullvad.net', 'au4-wg.socks5.mullvad.net', 'au1-wg.socks5.mullvad.net',
                      'au2-wg.socks5.mullvad.net', 'au8-wg.socks5.mullvad.net', 'au9-wg.socks5.mullvad.net',
                      'au10-wg.socks5.mullvad.net', 'au11-wg.socks5.mullvad.net', 'au12-wg.socks5.mullvad.net',
                      'au13-wg.socks5.mullvad.net', 'au14-wg.socks5.mullvad.net', 'at4-wg.socks5.mullvad.net',
                      'at5-wg.socks5.mullvad.net', 'at6-wg.socks5.mullvad.net', 'at7-wg.socks5.mullvad.net',
                      'at8-wg.socks5.mullvad.net', 'at9-wg.socks5.mullvad.net', 'be1-wg.socks5.mullvad.net',
                      'be2-wg.socks5.mullvad.net', 'be3-wg.socks5.mullvad.net', 'be4-wg.socks5.mullvad.net',
                      'br1-wg.socks5.mullvad.net', 'br3-wg.socks5.mullvad.net', 'bg4-wg.socks5.mullvad.net',
                      'bg5-wg.socks5.mullvad.net', 'bg6-wg.socks5.mullvad.net', 'bg7-wg.socks5.mullvad.net',
                      'ca10-wg.socks5.mullvad.net', 'ca11-wg.socks5.mullvad.net', 'ca12-wg.socks5.mullvad.net',
                      'ca13-wg.socks5.mullvad.net', 'ca14-wg.socks5.mullvad.net', 'ca15-wg.socks5.mullvad.net',
                      'ca16-wg.socks5.mullvad.net', 'ca17-wg.socks5.mullvad.net', 'ca18-wg.socks5.mullvad.net',
                      'ca19-wg.socks5.mullvad.net', 'ca20-wg.socks5.mullvad.net', 'ca21-wg.socks5.mullvad.net',
                      'ca22-wg.socks5.mullvad.net', 'ca23-wg.socks5.mullvad.net', 'ca24-wg.socks5.mullvad.net',
                      'ca25-wg.socks5.mullvad.net', 'ca26-wg.socks5.mullvad.net', 'ca27-wg.socks5.mullvad.net',
                      'cz1-wg.socks5.mullvad.net', 'cz2-wg.socks5.mullvad.net', 'cz3-wg.socks5.mullvad.net',
                      'cz4-wg.socks5.mullvad.net', 'cz5-wg.socks5.mullvad.net', 'dk2-wg.socks5.mullvad.net',
                      'dk3-wg.socks5.mullvad.net', 'dk5-wg.socks5.mullvad.net', 'dk6-wg.socks5.mullvad.net',
                      'dk7-wg.socks5.mullvad.net', 'dk8-wg.socks5.mullvad.net', 'ee1-wg.socks5.mullvad.net',
                      'ee2-wg.socks5.mullvad.net', 'ee3-wg.socks5.mullvad.net', 'fi1-wg.socks5.mullvad.net',
                      'fi2-wg.socks5.mullvad.net', 'fi3-wg.socks5.mullvad.net', 'fr15-wg.socks5.mullvad.net',
                      'fr16-wg.socks5.mullvad.net', 'fr4-wg.socks5.mullvad.net', 'fr5-wg.socks5.mullvad.net',
                      'fr6-wg.socks5.mullvad.net', 'fr7-wg.socks5.mullvad.net', 'fr8-wg.socks5.mullvad.net',
                      'fr10-wg.socks5.mullvad.net', 'fr11-wg.socks5.mullvad.net', 'fr12-wg.socks5.mullvad.net',
                      'fr13-wg.socks5.mullvad.net', 'fr14-wg.socks5.mullvad.net', 'de20-wg.socks5.mullvad.net',
                      'de21-wg.socks5.mullvad.net', 'de22-wg.socks5.mullvad.net', 'de4-wg.socks5.mullvad.net',
                      'de5-wg.socks5.mullvad.net', 'de7-wg.socks5.mullvad.net', 'de8-wg.socks5.mullvad.net',
                      'de10-wg.socks5.mullvad.net', 'de11-wg.socks5.mullvad.net', 'de12-wg.socks5.mullvad.net',
                      'de13-wg.socks5.mullvad.net', 'de14-wg.socks5.mullvad.net', 'de15-wg.socks5.mullvad.net',
                      'de16-wg.socks5.mullvad.net', 'de17-wg.socks5.mullvad.net', 'de23-wg.socks5.mullvad.net',
                      'de24-wg.socks5.mullvad.net', 'de25-wg.socks5.mullvad.net', 'de26-wg.socks5.mullvad.net',
                      'hk1-wg.socks5.mullvad.net', 'hk2-wg.socks5.mullvad.net', 'hk3-wg.socks5.mullvad.net',
                      'hk4-wg.socks5.mullvad.net', 'hu3-wg.socks5.mullvad.net', 'hu4-wg.socks5.mullvad.net',
                      'hu5-wg.socks5.mullvad.net', 'ie1-wg.socks5.mullvad.net', 'ie2-wg.socks5.mullvad.net',
                      'it4-wg.socks5.mullvad.net', 'it5-wg.socks5.mullvad.net', 'it6-wg.socks5.mullvad.net',
                      'it7-wg.socks5.mullvad.net', 'it8-wg.socks5.mullvad.net', 'jp1-wg.socks5.mullvad.net',
                      'jp2-wg.socks5.mullvad.net', 'jp3-wg.socks5.mullvad.net', 'jp4-wg.socks5.mullvad.net',
                      'jp6-wg.socks5.mullvad.net', 'jp7-wg.socks5.mullvad.net', 'jp8-wg.socks5.mullvad.net',
                      'jp9-wg.socks5.mullvad.net', 'jp10-wg.socks5.mullvad.net', 'jp11-wg.socks5.mullvad.net',
                      'jp12-wg.socks5.mullvad.net', 'jp13-wg.socks5.mullvad.net', 'lv1-wg.socks5.mullvad.net',
                      'lu1-wg.socks5.mullvad.net', 'lu2-wg.socks5.mullvad.net', 'md1-wg.socks5.mullvad.net',
                      'nl1-wg.socks5.mullvad.net', 'nl2-wg.socks5.mullvad.net', 'nl3-wg.socks5.mullvad.net',
                      'nl4-wg.socks5.mullvad.net', 'nl5-wg.socks5.mullvad.net', 'nl20-wg.socks5.mullvad.net',
                      'nl21-wg.socks5.mullvad.net', 'nl22-wg.socks5.mullvad.net', 'nl23-wg.socks5.mullvad.net',
                      'nz1-wg.socks5.mullvad.net', 'nz2-wg.socks5.mullvad.net', 'mk1-wg.socks5.mullvad.net',
                      'no1-wg.socks5.mullvad.net', 'no2-wg.socks5.mullvad.net', 'no3-wg.socks5.mullvad.net',
                      'no4-wg.socks5.mullvad.net', 'pl1-wg.socks5.mullvad.net', 'pl2-wg.socks5.mullvad.net',
                      'pl3-wg.socks5.mullvad.net', 'pl4-wg.socks5.mullvad.net', 'pt1-wg.socks5.mullvad.net',
                      'pt2-wg.socks5.mullvad.net', 'ro4-wg.socks5.mullvad.net', 'ro5-wg.socks5.mullvad.net',
                      'ro6-wg.socks5.mullvad.net', 'ro7-wg.socks5.mullvad.net', 'ro8-wg.socks5.mullvad.net',
                      'rs3-wg.socks5.mullvad.net', 'rs4-wg.socks5.mullvad.net', 'sg4-wg.socks5.mullvad.net',
                      'sg5-wg.socks5.mullvad.net', 'sg6-wg.socks5.mullvad.net', 'sg7-wg.socks5.mullvad.net',
                      'sg8-wg.socks5.mullvad.net', 'es1-wg.socks5.mullvad.net', 'es2-wg.socks5.mullvad.net',
                      'es4-wg.socks5.mullvad.net', 'es5-wg.socks5.mullvad.net', 'se3-wg.socks5.mullvad.net',
                      'se5-wg.socks5.mullvad.net', 'se9-wg.socks5.mullvad.net', 'se10-wg.socks5.mullvad.net',
                      'se1-wg.socks5.mullvad.net', 'se4-wg.socks5.mullvad.net', 'se15-wg.socks5.mullvad.net',
                      'se17-wg.socks5.mullvad.net', 'se18-wg.socks5.mullvad.net', 'se19-wg.socks5.mullvad.net',
                      'se21-wg.socks5.mullvad.net', 'se22-wg.socks5.mullvad.net', 'se23-wg.socks5.mullvad.net',
                      'se2-wg.socks5.mullvad.net', 'se6-wg.socks5.mullvad.net', 'se7-wg.socks5.mullvad.net',
                      'se8-wg.socks5.mullvad.net', 'se13-wg.socks5.mullvad.net', 'se14-wg.socks5.mullvad.net',
                      'se26-wg.socks5.mullvad.net', 'se27-wg.socks5.mullvad.net', 'se28-wg.socks5.mullvad.net',
                      'ch2-wg.socks5.mullvad.net', 'ch5-wg.socks5.mullvad.net', 'ch6-wg.socks5.mullvad.net',
                      'ch7-wg.socks5.mullvad.net', 'ch8-wg.socks5.mullvad.net', 'ch9-wg.socks5.mullvad.net',
                      'ch10-wg.socks5.mullvad.net', 'ch11-wg.socks5.mullvad.net', 'ch12-wg.socks5.mullvad.net',
                      'ch13-wg.socks5.mullvad.net', 'ch14-wg.socks5.mullvad.net', 'ch15-wg.socks5.mullvad.net',
                      'ch16-wg.socks5.mullvad.net', 'ch17-wg.socks5.mullvad.net', 'gb4-wg.socks5.mullvad.net',
                      'gb5-wg.socks5.mullvad.net', 'gb11-wg.socks5.mullvad.net', 'gb12-wg.socks5.mullvad.net',
                      'gb13-wg.socks5.mullvad.net', 'gb14-wg.socks5.mullvad.net', 'gb15-wg.socks5.mullvad.net',
                      'gb16-wg.socks5.mullvad.net', 'gb17-wg.socks5.mullvad.net', 'gb18-wg.socks5.mullvad.net',
                      'gb19-wg.socks5.mullvad.net', 'gb20-wg.socks5.mullvad.net', 'gb33-wg.socks5.mullvad.net',
                      'gb34-wg.socks5.mullvad.net', 'gb35-wg.socks5.mullvad.net', 'gb36-wg.socks5.mullvad.net',
                      'gb22-wg.socks5.mullvad.net', 'gb24-wg.socks5.mullvad.net', 'gb25-wg.socks5.mullvad.net',
                      'gb26-wg.socks5.mullvad.net', 'gb27-wg.socks5.mullvad.net', 'gb28-wg.socks5.mullvad.net',
                      'gb29-wg.socks5.mullvad.net', 'gb30-wg.socks5.mullvad.net', 'gb31-wg.socks5.mullvad.net',
                      'gb32-wg.socks5.mullvad.net', 'us167-wg.socks5.mullvad.net', 'us168-wg.socks5.mullvad.net',
                      'us169-wg.socks5.mullvad.net', 'us170-wg.socks5.mullvad.net', 'us171-wg.socks5.mullvad.net',
                      'us172-wg.socks5.mullvad.net', 'us173-wg.socks5.mullvad.net', 'us174-wg.socks5.mullvad.net',
                      'us175-wg.socks5.mullvad.net', 'us176-wg.socks5.mullvad.net', 'us233-wg.socks5.mullvad.net',
                      'us234-wg.socks5.mullvad.net', 'us243-wg.socks5.mullvad.net', 'us4-wg.socks5.mullvad.net',
                      'us18-wg.socks5.mullvad.net', 'us22-wg.socks5.mullvad.net', 'us23-wg.socks5.mullvad.net',
                      'us128-wg.socks5.mullvad.net', 'us129-wg.socks5.mullvad.net', 'us130-wg.socks5.mullvad.net',
                      'us131-wg.socks5.mullvad.net', 'us132-wg.socks5.mullvad.net', 'us133-wg.socks5.mullvad.net',
                      'us231-wg.socks5.mullvad.net', 'us232-wg.socks5.mullvad.net', 'us244-wg.socks5.mullvad.net',
                      'us245-wg.socks5.mullvad.net', 'us17-wg.socks5.mullvad.net', 'us30-wg.socks5.mullvad.net',
                      'us31-wg.socks5.mullvad.net', 'us32-wg.socks5.mullvad.net', 'us33-wg.socks5.mullvad.net',
                      'us34-wg.socks5.mullvad.net', 'us35-wg.socks5.mullvad.net', 'us36-wg.socks5.mullvad.net',
                      'us37-wg.socks5.mullvad.net', 'us38-wg.socks5.mullvad.net', 'us39-wg.socks5.mullvad.net',
                      'us143-wg.socks5.mullvad.net', 'us144-wg.socks5.mullvad.net', 'us145-wg.socks5.mullvad.net',
                      'us146-wg.socks5.mullvad.net', 'us147-wg.socks5.mullvad.net', 'us148-wg.socks5.mullvad.net',
                      'us149-wg.socks5.mullvad.net', 'us150-wg.socks5.mullvad.net', 'us151-wg.socks5.mullvad.net',
                      'us152-wg.socks5.mullvad.net', 'us153-wg.socks5.mullvad.net', 'us154-wg.socks5.mullvad.net',
                      'us235-wg.socks5.mullvad.net', 'us236-wg.socks5.mullvad.net', 'us240-wg.socks5.mullvad.net',
                      'us10-wg.socks5.mullvad.net', 'us11-wg.socks5.mullvad.net', 'us12-wg.socks5.mullvad.net',
                      'us44-wg.socks5.mullvad.net', 'us45-wg.socks5.mullvad.net', 'us46-wg.socks5.mullvad.net',
                      'us47-wg.socks5.mullvad.net', 'us48-wg.socks5.mullvad.net', 'us49-wg.socks5.mullvad.net',
                      'us50-wg.socks5.mullvad.net', 'us51-wg.socks5.mullvad.net', 'us52-wg.socks5.mullvad.net',
                      'us53-wg.socks5.mullvad.net', 'us54-wg.socks5.mullvad.net', 'us55-wg.socks5.mullvad.net',
                      'us56-wg.socks5.mullvad.net', 'us57-wg.socks5.mullvad.net', 'us58-wg.socks5.mullvad.net',
                      'us59-wg.socks5.mullvad.net', 'us60-wg.socks5.mullvad.net', 'us61-wg.socks5.mullvad.net',
                      'us62-wg.socks5.mullvad.net', 'us63-wg.socks5.mullvad.net', 'us64-wg.socks5.mullvad.net',
                      'us65-wg.socks5.mullvad.net', 'us66-wg.socks5.mullvad.net', 'us67-wg.socks5.mullvad.net',
                      'us68-wg.socks5.mullvad.net', 'us69-wg.socks5.mullvad.net', 'us70-wg.socks5.mullvad.net',
                      'us71-wg.socks5.mullvad.net', 'us229-wg.socks5.mullvad.net', 'us230-wg.socks5.mullvad.net',
                      'us239-wg.socks5.mullvad.net', 'us155-wg.socks5.mullvad.net', 'us156-wg.socks5.mullvad.net',
                      'us157-wg.socks5.mullvad.net', 'us158-wg.socks5.mullvad.net', 'us159-wg.socks5.mullvad.net',
                      'us160-wg.socks5.mullvad.net', 'us161-wg.socks5.mullvad.net', 'us162-wg.socks5.mullvad.net',
                      'us163-wg.socks5.mullvad.net', 'us164-wg.socks5.mullvad.net', 'us165-wg.socks5.mullvad.net',
                      'us166-wg.socks5.mullvad.net', 'us225-wg.socks5.mullvad.net', 'us226-wg.socks5.mullvad.net',
                      'us72-wg.socks5.mullvad.net', 'us73-wg.socks5.mullvad.net', 'us74-wg.socks5.mullvad.net',
                      'us75-wg.socks5.mullvad.net', 'us76-wg.socks5.mullvad.net', 'us77-wg.socks5.mullvad.net',
                      'us78-wg.socks5.mullvad.net', 'us79-wg.socks5.mullvad.net', 'us80-wg.socks5.mullvad.net',
                      'us81-wg.socks5.mullvad.net', 'us82-wg.socks5.mullvad.net', 'us83-wg.socks5.mullvad.net',
                      'us84-wg.socks5.mullvad.net', 'us85-wg.socks5.mullvad.net', 'us86-wg.socks5.mullvad.net',
                      'us87-wg.socks5.mullvad.net', 'us88-wg.socks5.mullvad.net', 'us89-wg.socks5.mullvad.net',
                      'us90-wg.socks5.mullvad.net', 'us91-wg.socks5.mullvad.net', 'us92-wg.socks5.mullvad.net',
                      'us93-wg.socks5.mullvad.net', 'us95-wg.socks5.mullvad.net', 'us96-wg.socks5.mullvad.net',
                      'us97-wg.socks5.mullvad.net', 'us98-wg.socks5.mullvad.net', 'us99-wg.socks5.mullvad.net',
                      'us101-wg.socks5.mullvad.net', 'us102-wg.socks5.mullvad.net', 'us103-wg.socks5.mullvad.net',
                      'us104-wg.socks5.mullvad.net', 'us105-wg.socks5.mullvad.net', 'us106-wg.socks5.mullvad.net',
                      'us107-wg.socks5.mullvad.net', 'us108-wg.socks5.mullvad.net', 'us109-wg.socks5.mullvad.net',
                      'us110-wg.socks5.mullvad.net', 'us111-wg.socks5.mullvad.net', 'us112-wg.socks5.mullvad.net',
                      'us113-wg.socks5.mullvad.net', 'us114-wg.socks5.mullvad.net', 'us115-wg.socks5.mullvad.net',
                      'us116-wg.socks5.mullvad.net', 'us117-wg.socks5.mullvad.net', 'us118-wg.socks5.mullvad.net',
                      'us119-wg.socks5.mullvad.net', 'us120-wg.socks5.mullvad.net', 'us121-wg.socks5.mullvad.net',
                      'us122-wg.socks5.mullvad.net', 'us123-wg.socks5.mullvad.net', 'us124-wg.socks5.mullvad.net',
                      'us125-wg.socks5.mullvad.net', 'us126-wg.socks5.mullvad.net', 'us127-wg.socks5.mullvad.net',
                      'us189-wg.socks5.mullvad.net', 'us190-wg.socks5.mullvad.net', 'us191-wg.socks5.mullvad.net',
                      'us192-wg.socks5.mullvad.net', 'us193-wg.socks5.mullvad.net', 'us194-wg.socks5.mullvad.net',
                      'us183-wg.socks5.mullvad.net', 'us184-wg.socks5.mullvad.net', 'us185-wg.socks5.mullvad.net',
                      'us186-wg.socks5.mullvad.net', 'us187-wg.socks5.mullvad.net', 'us134-wg.socks5.mullvad.net',
                      'us135-wg.socks5.mullvad.net', 'us136-wg.socks5.mullvad.net', 'us137-wg.socks5.mullvad.net',
                      'us138-wg.socks5.mullvad.net', 'us139-wg.socks5.mullvad.net', 'us140-wg.socks5.mullvad.net',
                      'us141-wg.socks5.mullvad.net', 'us142-wg.socks5.mullvad.net', 'us195-wg.socks5.mullvad.net',
                      'us196-wg.socks5.mullvad.net', 'us197-wg.socks5.mullvad.net', 'us198-wg.socks5.mullvad.net',
                      'us199-wg.socks5.mullvad.net', 'us200-wg.socks5.mullvad.net', 'us201-wg.socks5.mullvad.net',
                      'us202-wg.socks5.mullvad.net', 'us203-wg.socks5.mullvad.net', 'us204-wg.socks5.mullvad.net',
                      'us205-wg.socks5.mullvad.net', 'us206-wg.socks5.mullvad.net', 'us207-wg.socks5.mullvad.net',
                      'us208-wg.socks5.mullvad.net', 'us177-wg.socks5.mullvad.net', 'us178-wg.socks5.mullvad.net',
                      'us179-wg.socks5.mullvad.net', 'us180-wg.socks5.mullvad.net', 'us181-wg.socks5.mullvad.net',
                      'us182-wg.socks5.mullvad.net', 'us209-wg.socks5.mullvad.net', 'us210-wg.socks5.mullvad.net',
                      'us213-wg.socks5.mullvad.net', 'us214-wg.socks5.mullvad.net', 'us215-wg.socks5.mullvad.net',
                      'us216-wg.socks5.mullvad.net', 'us227-wg.socks5.mullvad.net', 'us228-wg.socks5.mullvad.net',
                      'us237-wg.socks5.mullvad.net', 'us238-wg.socks5.mullvad.net', 'us241-wg.socks5.mullvad.net', ]
        self.countries = ['gb', 'de', 'ca', 'cz', 'bg', 'it', 'lv', 'ch', 'dk', 'br', 'at', 'fi', 'se', 'us', 'mk',
                          'au', 'lu', 'hk', 'no', 'ro', 'jp', 'ie', 'pt', 'pl', 'rs', 'es', 'hu', 'ee', 'md', 'sg',
                          'nl', 'fr', 'be', 'nz']

    @staticmethod
    def ip():
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        return local_ip

    @staticmethod
    def isConnect():
        return False if "192.168" in Mullvad.ip() else True

    @staticmethod
    def check_status():
        return subprocess.run("mullvad status", shell=True)

    def random_proxy_server(self):
        return random.choice(self.socks)

    def proxy(self, n):
        return self.socks[n]

    def random_country(self):
        return random.choice(self.countries)

    def change_country(self, country: str):
        self.country = country

    def allservers(self):
        return self.socks

    def allcountries(self):
        return self.countries

    def connect(self):
        orig = Mullvad.ip()
        if self.country is None:
            self.change_country(self.random_country())
        subprocess.run(f"mullvad relay set location {self.country}", stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
        subprocess.run("mullvad connect", shell=True)
        self._poll(orig)

    def disconnect(self):
        orig = Mullvad.ip()
        subprocess.run("mullvad disconnect", shell=True)
        self._poll(orig)

    def _poll(self, orig):
        for i in range(self.timeout):
            if orig != Mullvad.ip():
                break
            elif i == self.timeout - 1:
                return False
            time.sleep(1)
        return True


if __name__ == '__main__':
    vpn = Mullvad()
    print(vpn.allcountries())
    vpn.change_country(vpn.random_country())
    print(vpn.ip())
    vpn.connect()
