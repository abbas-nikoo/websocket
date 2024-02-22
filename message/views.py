# import requests

from django.http import JsonResponse
# from ipware import get_client_ip
# from rest_framework import status
# def get_country(request):
#     # دریافت IP مخاطب
#     client_ip, is_routable = get_client_ip(request)
#
#     # درخواست به سرویس ipinfo.io
#     response = requests.get(f"https://ipinfo.io/{client_ip}/country")
#     print('###################')
#     # if response.status_code == 200:
#     print('###################')
#
#     country_code = response.text.strip()
#     data = {
#         'country_code': country_code,
#         'message': 'کشور شما تشخیص داده شد.'
#     }
#     return JsonResponse(data)
#     # else:
#     #     data = {
#     #         'error': 'خطا در تشخیص کشور.'
#     #     }
#     #     return JsonResponse(data, status=500)
#
# # سایر کدها
#
#
# from django.http import JsonResponse
# from geopy.geocoders import Nominatim
#
#
# def get_country(request):
#     # دریافت IP مخاطب
#     client_ip, is_routable = get_client_ip(request)
#
#     # تشخیص کشور بر اساس IP مخاطب با استفاده از geopy
#     geolocator = Nominatim(user_agent="geoapiExercises")
#     location = geolocator.reverse(client_ip, exactly_one=True)
#     print('###################')
#
#     if location:
#         country_code = location.raw.get('address', {}).get('country_code')
#         if country_code:
#             data = {
#                 'country_code': country_code,
#                 'message': 'کشور شما تشخیص داده شد.'
#             }
#             return JsonResponse(data)
#
#     data = {
#         'error': 'خطا در تشخیص کشور.'
#     }
#     return JsonResponse(data, status=500)

#
# import requests
# from geopy.geocoders import Nominatim
#
#
# def get_coordinates(ip):
#     # تبدیل IP به مختصات
#     response = requests.get(f"http://ip-api.com/json/{ip}")
#     data = response.json()
#     latitude = data.get("lat")
#     longitude = data.get("lon")
#
#     if latitude and longitude:
#         return latitude, longitude
#     else:
#         return None
#
#
# def get_country(request):
#     # دریافت IP مخاطب
#     client_ip, is_routable = get_client_ip(request)
#
#     if client_ip:
#         # تبدیل IP به مختصات
#         coordinates = get_coordinates(client_ip)
#         print('###################')
#     # if coordinates:
#         # تشخیص کشور بر اساس مختصات
#         geolocator = Nominatim(user_agent="geoapiExercises")
#         location = geolocator.reverse(coordinates, exactly_one=True)
#
#         if location:
#             country_code = location.raw.get('address', {}).get('country_code')
#             if country_code:
#                 data = {
#                     'country_code': country_code,
#                     'message': 'کشور شما تشخیص داده شد.'
#                 }
#                 return JsonResponse(data)
#
#     data = {
#         'error': 'خطا در تشخیص کشور.'
#     }
#     return JsonResponse(data, status=500)

import requests

# def get_country(ip):
#     try:
#         response = requests.get(f"http://ip-api.com/json/{ip}")
#         data = response.json()
#         country_code = data.get("countryCode")
#         return country_code
#     except Exception as e:
#         return None
#
# # مثال استفاده:
# ip_address = "8.8.8.8"  # آدرس IP مورد نظر را قرار دهید
# country_code = get_country(ip_address)
# if country_code:
#     print(f"کد کشور: {country_code}")
#
# else:
#     print("خطا در تشخیص کشور")


# from django.http import JsonResponse
# from django.contrib.gis.geoip2 import GeoIP2
#
# def get_country(request):
#     # ساخت یک نمونه از کتابخانه GeoIP
#     geoip = GeoIP2()
#
#     # دریافت IP درخواست کننده (مثلاً از request.META)
#     user_ip = get_client_ip(request)
#
#     # تشخیص کشور بر اساس IP
#     country = geoip.country(user_ip)
#
#     # ارسال کشور به عنوان JSON
#     return JsonResponse({'country': country})
#
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


# from django.http import JsonResponse
# from django.contrib.gis.geoip2 import GeoIP2
#
# def get_country(request):
#     # ساخت یک نمونه از کتابخانه GeoIP
#     geoip = GeoIP2()
#
#     # دریافت IP درخواست کننده (مثلاً از request.META)
#     user_ip = get_client_ip(request)
#
#     # تشخیص کشور بر اساس IP
#     country = geoip.country(user_ip)
#
#     # ارسال کشور به عنوان JSON
#     return JsonResponse({'country': country})
#
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
# from ipware import get_client_ip
# def get_country(request):
#     ip, is_routable = get_client_ip(request)
#
#     print(ip)

# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# import requests
#
# class CountryCodeView(APIView):
#     def get(self, request):
#         # دریافت آی‌پی کاربر از ریکوئست
#         user_ip = self.get_client_ip(request)
#
#         # فراخوانی API برای دریافت اطلاعات کشور
#         country_info = self.get_country_info(user_ip)
#
#         if country_info:
#             # اگر اطلاعات کشور موجود باشد، کد کشور را ارسال کنید
#             return Response({'country_code': user_ip['country_code']})
#         else:
#             return Response({'error': 'Unable to retrieve country code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     def get_client_ip(self, request):
#         x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#         if x_forwarded_for:
#             ip = x_forwarded_for.split(',')[0]
#         else:
#             ip = request.META.get('REMOTE_ADDR')
#         return ip
#
#     def get_country_info(self, ip):
#         # ارسال درخواست به سرویس API برای دریافت اطلاعات کشور
#         try:
#             response = requests.get(f'https://ip-api.com/json/{ip}')
#             response.raise_for_status()
#             data = response.json()
#             if data['status'] == 'success':
#                 return {'country_code': data['countryCode']}
#             else:
#                 return None
#         except requests.exceptions.RequestException:
#             return None


# در فایل views.py
# from django.contrib.gis.geoip2 import GeoIP2
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from ipware import get_client_ip
# class CountryCodeView(APIView):
#     def get(self, request):
#         user_ip = get_client_ip(request)
#         print(user_ip)
#         country_code = self.get_country_code(user_ip)
#
#         if country_code:
#             return Response({'country_code': country_code})
#         else:
#             return Response({'error': 'Unable to retrieve country code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#     # def get_client_ip(self, request):
#     #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     #     if x_forwarded_for:
#     #         ip = x_forwarded_for.split(',')[0]
#     #     else:
#     #         ip = request.META.get('REMOTE_ADDR')
#     #     return ip
#
#     def get_country_code(self, ip):
#         try:
#             g = GeoIP2()
#             country_code = g.country(ip)['country_code']
#             return country_code
#         except Exception:
#             return None


# from django.contrib.gis.geoip2 import GeoIP2
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.decorators import api_view
# from ipware import get_client_ip
#
#
# @api_view(['GET'])
# def get_country_code(request):
#     # دریافت آی‌پی کاربر از ریکوئست
#     user_ip = get_client_ip(request)
#
#     # دریافت کد کشور با استفاده از GeoIP
#     country_code = get_country_code(user_ip)
#
#     if country_code:
#         # اگر کد کشور موجود باشد، آن را ارسال کنید
#         return Response({'country_code': country_code})
#     else:
#         return Response({'error': 'Unable to retrieve country code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip


# def get_country_code(request):
#     try:
#         g = GeoIP2()
#         country_code = g.country(request.META.get('REMOTE_ADDR'))['country_code']
#         return Response({'country_code': country_code})
#     except requests.exceptions.RequestException:
#         return None

# def get_country_code(request):
#     try:
#         g = GeoIP2()
#         user_ip = request.META.get('REMOTE_ADDR')
#         country_code = g.country(user_ip)['country_code']
#         return Response({'country_code': country_code})
#     except requests.exceptions.RequestException:
#         return None

# # در فایل views.py
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# import requests
# # from ipware import get_client_ip
#
# @api_view(['GET'])
# def get_country_code(request):
#     # دریافت آی‌پی کاربر از ریکوئست
#     user_ip = get_client_ip(request)
#     print(user_ip)
#     # فراخوانی API برای دریافت اطلاعات کشور
#     country_info = get_country_info(user_ip)
#
#     if country_info:
#         # اگر اطلاعات کشور موجود باشد، کد کشور را ارسال کنید
#         return Response({'country_code': country_info['country_code']})
#     else:
#         return Response({'error': 'Unable to retrieve country code'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# def get_client_ip(request):
#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     return ip
#
#
# def get_country_info(ip):
#     # ارسال درخواست به سرویس API برای دریافت اطلاعات کشور
#     try:
#         response = requests.get(f'https://ip-api.com/json/{ip}')
#         response.raise_for_status()
#         data = response.json()
#         if data['status'] == 'success':
#             return {'country_code': data['countryCode']}
#         else:
#             return None
#     except requests.exceptions.RequestException:
#         return None


# import requests
#
#
# def get_location_info(ip):
#     try:
#         # توکن API رایگان خود را در اینجا قرار دهید
#         api_token = '9b769b409d187a1a774c953035e955f9'
#
#         # ساخت URL برای درخواست به ip-api.com API
#         url = f'http://ip-api.com/json/{ip}?fields=66842623&lang=en&token={api_token}'
#
#         headers = {
#             'X-Frame-Options': 'SAMEORIGIN',
#         }
#
#         # ارسال درخواست به ip-api.com
#         response = requests.get(url, headers=headers)
#
#         # بررسی و بازگرداندن اطلاعات مکان اگر درخواست موفق باشد
#         if response.status_code == 200:
#             data = response.json()
#             return {
#                 'ip': data.get('query'),
#                 'city': data.get('city'),
#                 'region': data.get('regionName'),
#                 'country': data.get('country'),
#                 'location': f'{data.get("lat")}, {data.get("lon")}'
#             }
#         else:
#             return None
#     except Exception as e:
#         return None


# import requests
# from ipware import get_client_ip
# from django.http import HttpResponse
#
#
# def get_location_info(request):
#     try:
#         # توکن API رایگان خود را در اینجا قرار دهید
#         api_token = '9b769b409d187a1a774c953035e955f9'
#
#         # دریافت IP کاربر از درخواست با استفاده از ipware
#         client_ip = get_client_ip(request)
#         print(client_ip)
#         # ساخت URL برای درخواست به ip-api.com API با استفاده از IP از درخواست
#         url = f'http://ip-api.com/json/{client_ip}?fields=66842623&lang=en&token={api_token}'
#
#         # ارسال درخواست به ip-api.com
#         response = requests.get(url)
#         print(client_ip)
#         print(response)
#         # بررسی و بازگرداندن اطلاعات مکان اگر درخواست موفق باشد
#         if response.status_code == 200:
#             data = response.json()
#             response_data = {
#                 'ip': data.get('query'),
#                 'city': data.get('city'),
#                 'region': data.get('regionName'),
#                 'country': data.get('country'),
#                 'location': f'{data.get("lat")}, {data.get("lon")}'
#             }
#
#             response = HttpResponse()
#             response['X-Frame-Options'] = 'DENY'  # یکی از مقادیر ممکن برای X-Frame-Options
#             return (response_data)
#         else:
#             return None
#     except Exception as e:
#         return None

# import requests
# from ipware import get_client_ip
#
# def get_location_info(request):
#     try:
#         # توکن API رایگان خود را در اینجا قرار دهید
#         api_token = '9b769b409d187a1a774c953035e955f9'
#
#         # دریافت IP کاربر از درخواست با استفاده از ipware
#         client_ip, _ = get_client_ip(request)
#
#         # ساخت URL برای درخواست به ip-api.com API با استفاده از IP از درخواست
#         url = f'http://api.ipapi.com/{client_ip}?access_key={api_token}'
#
#         # ارسال درخواست به سرویس ipapi
#         response = requests.get(url)
#
#         # بررسی و بازگرداندن اطلاعات مکان اگر درخواست موفق باشد
#         if response.status_code == 200:
#             data = response.json()
#             return {
#                 'ip': data.get('ip'),
#                 'city': data.get('city'),
#                 'region': data.get('region_name'),
#                 'country': data.get('country_name'),
#                 'location': f'{data.get("latitude")}, {data.get("longitude")}'
#             }
#         else:
#             return None
#     except Exception as e:
#         return None


# import requests
#
# def get_location_info(request):
#
# # تنظیم آدرس IP و کلید دسترسی API
#     ip = '161.185.160.93'
#     access_key = '9b769b409d187a1a774c953035e955f9'
#
#     try:
#         # ساخت URL برای درخواست به سرویس ipapi با استفاده از IP و کلید دسترسی
#         url = f'http://api.ipapi.com/{ip}?access_key={access_key}'
#
#
#         # ارسال درخواست به سرویس ipapi
#         response = requests.get(url)
#
#         # بررسی و پردازش پاسخ JSON
#         if response.status_code == 200:
#             api_result = response.json()
#             calling_code = api_result.get('location', {}).get('calling_code')
#             if calling_code:
#                 return {'calling_code': calling_code}
#             else:
#                 return None
#         else:
#             return None
#     except Exception as e:
#         return None


import requests
import json
from rest_framework import status
from ipware import get_client_ip
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_location_info(request):
    ip = get_client_ip(request)
    access_key = '0d9ff25a2b9e9e0a6d79828f16b9b8a2'
    print(ip)
    try:
        url = f'http://api.ipapi.com/{ip}?access_key={access_key}'

        # Set headers before sending the request

        response = requests.get(url)
        print(response)
        if response.status_code == 200:
            print(response.text)
            api_result = json.loads(response.text)

            calling_code = api_result["country_code"]
            if calling_code:
                return Response({'calling_code': calling_code}, status=status.HTTP_200_OK)
            else:
                return Response( status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        return Response(status=status.HTTP_502_BAD_GATEWAY)





# def get_location_info(request):
#     ip = '161.185.160.93'
#     access_key = '9b769b409d187a1a774c953035e955f9'
#
#     try:
#         url = f'http://api.ipapi.com/{ip}?access_key={access_key}'
#
#         # Set headers before sending the request
#
#         response = requests.get(url)
#         print(response)
#         if response.status_code == 200:
#             print(response.text)
#             api_result = json.loads(response.text)
#             print(api_result["country_code"])


    #         calling_code = api_result["country_code"]
    #         if calling_code:
    #             return Response({'calling_code': calling_code}, status=status.HTTP_200_OK)
    #         else:
    #             return None
    #     else:
    #         return None
    # except Exception as e:
    #     return None