from router import routes
from utils import extract_physic_mode
from wrappers import BaseRequest

test_requests = [
    '0 0.0.0.0:1234 "jesus" wr',
    '0 0.0.0.0:1234 "jesus" wr hunterun-19',
    '0 0.0.0.0:1234 "jesus" wr hunterun-19 vq3',
    '0 0.0.0.0:1234 "jesus" wr hunterun-19 cpm',
    '0 0.0.0.0:1234 "jesus" wr 13vast cpm.2',
    '0 0.0.0.0:1234 "jesus" wr 13vast cpm.3',
    '0 0.0.0.0:1234 "jesus" wr 13vast vq3.3',
    '0 0.0.0.0:1234 "jesus" wr doesnotexist',
    '0 0.0.0.0:1234 "jesus" topspeed',
    '0 0.0.0.0:1234 "jesus" topspeed',
    '0 0.0.0.0:1234 "jesus" topspeed pornstar-slopin',
    '0 0.0.0.0:1234 "jesus" topspeed pornstar-17percent',
    '0 0.0.0.0:1234 "jesus" topspeed doesnotexist',
    '0 0.0.0.0:1234 "jesus" topspeed 13vast cpm.2',
    '0 0.0.0.0:1234 "jesus" topspeed 13vast vq3.2',
    '0 0.0.0.0:1234 "jesus" topspeed 13vast cpm.3',
    '0 0.0.0.0:1234 "jesus" topspeed 13vast vq3.3',
    '0 0.0.0.0:1234 "jesus" pr doesnotexist',
    '0 0.0.0.0:1234 "jesus" pr',
    '0 0.0.0.0:1234 "jesus" pr cpm',
    '0 0.0.0.0:1234 "jesus" pr cpm +',
    '0 0.0.0.0:1234 "jesus" pr vq3',
    '0 0.0.0.0:1234 "jesus" pr hunterun-19 vq3',
    '0 0.0.0.0:1234 "jesus" pr pornstar-slopin',
    '0 0.0.0.0:1234 "jesus" pr pornstar-slopin show',
    '0 0.0.0.0:1234 "jesus" setpass waza',
    '0 0.0.0.0:1234 "jesus" rank',
    '0 0.0.0.0:1234 "jesus" rank 3',
    '0 0.0.0.0:1234 "jesus" rank pornstar-slopin',
    '0 0.0.0.0:1234 "jesus" rank pornstar-slopin 3',
    '0 0.0.0.0:1234 "jesus" rank 3 pornstar-slopin',
    '0 0.0.0.0:1234 "jesus" rank 3 pornstar-slopin cpm',
    '0 0.0.0.0:1234 "jesus" rank 3 pornstar-slopin vq3',
    '0 0.0.0.0:1234 "jesus" rank 3 cpm pornstar-slopin 4',
    '0 0.0.0.0:1234 "jesus" rank 4 cpm pornstar-slopin 3',
    '0 0.0.0.0:1234 "jesus" rank vq3 pornstar-slopin 3',
    '0 0.0.0.0:1234 "jesus" pr hunterun-19 vq3',
    '0 0.0.0.0:1234 "jesus" pr hunterun-19 vq3 +',
    '0 0.0.0.0:1234 "jesus" pr hunterun-19 vq3 ++',
    '0 0.0.0.0:1234 "jesus" pr hunterun-19 vq3 startat14 ++',
    '0 0.0.0.0:1234 "jesus" random',
    '0 0.0.0.0:1234 "jesus" random 3',
    '0 0.0.0.0:1234 "jesus" random pornstar',
    '0 0.0.0.0:1234 "jesus" random hun',
    '0 0.0.0.0:1234 "jesus" random ctf',
    '0 0.0.0.0:1234 "jesus" random st',
    '0 0.0.0.0:1234 "jesus" user jesus timehistory',
    '0 0.0.0.0:1234 "jesus" timehistory',
    '0 0.0.0.0:1234 "jesus" timehistory jesus',
    '0 0.0.0.0:1234 "jesus" time arcaon',
    '0 0.0.0.0:1234 "jesus" login mypassword',
    '0 0.0.0.0:1234 "jesus" login myusername mypassword',
    '0 0.0.0.0:1234 "jesus" time arcaon pornstar-slopin',
    '0 0.0.0.0:1234 "jesus" time cpm arcaon pornstar-slopin',

]



def test_extract_physic_mode():
    assert extract_physic_mode('cpm') == {'physic': 1, 'mode': -1}
    assert extract_physic_mode('vq3') == {'physic': 0, 'mode': -1}
    assert extract_physic_mode('vq3.-1') == {'physic': 0, 'mode': -1}
    assert extract_physic_mode('vq3.2') == {'physic': 0, 'mode': 2}
    assert extract_physic_mode('vq3.3') == {'physic': 0, 'mode': 3}
    assert extract_physic_mode('cpm.3') == {'physic': 1, 'mode': 3}

import commands

for raw in test_requests:
    request = BaseRequest(raw)
    print 'RAW: ', raw
    print 'Result:', routes[request.command](request)
    print 55*'-'
