import os
import time
import logging

from pathlib import Path
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from seleniumwire.webdriver import Chrome, ChromeOptions,\
                                   Firefox, FirefoxOptions


class Bot(object):
    def run(urls,
            browser,
            proxies,
            referers,
            user_agents,
            duration,
            executable_path,
            extension_path):
        logging.basicConfig(level=logging.CRITICAL)
        while True:
            try:
                seleniumwire_options = {'proxy': proxies.get(),
                                        'connection_timeout': None,
                                        'verify_ssl': False}
                user_agent = user_agents.get()
                if browser == 'chrome':
                    options = ChromeOptions()
                    options.add_argument('--no-sandbox')
                    options.add_argument('--mute-audio')
                    options.add_argument('--disable-gpu')
                    options.add_argument('--disable-dev-shm-usage')
                    options.add_argument(f'--user-agent={user_agent}')
                    options.add_experimental_option('excludeSwitches',
                                                    ['enable-logging'])
                    options.add_extension(extension_path)
                    WebDriver = Chrome
                else:
                    options = FirefoxOptions()
                    options.add_argument('--headless')
                    options.preferences.update({
                        'media.volume_scale': '0.0',
                        'media.peerconnection.enabled': False,
                        'general.useragent.override': user_agent
                    })
                    WebDriver = Firefox
                driver = WebDriver(executable_path=executable_path,
                                   options=options,
                                   service_log_path=os.devnull,
                                   seleniumwire_options=seleniumwire_options)
                driver.minimize_window()
                driver.header_overrides = {'Referer': referers.get()}
                driver.set_page_load_timeout(60)
                url = urls.get()
                try:
                    driver.get(url[0])
                except Exception:
                    pass
                finally:
                    if driver.title.endswith('YouTube'):
                        try:
                            WebDriverWait(
                                driver,
                                3
                            ).until(
                                EC.element_to_be_clickable(
                                    (By.CLASS_NAME,
                                     'ytp-large-play-button')
                                )
                            ).click()
                        except:
                            pass
                        finally:
                            if duration:
                                time.sleep(duration)
                            else:
                                video=WebDriverWait(
                                    driver,
                                    3
                                ).until(
                                    EC.presence_of_element_located(
                                        (By.CLASS_NAME,
                                         'html5-main-video')
                                    )
                                )
                                video_duration=driver.execute_script(
                                    'return arguments[0].getDuration()',
                                    video
                                )
                                time.sleep(float(video_duration)
                                           *random.uniform(0.35,
                                                           0.85))
            except Exception:
                pass
            finally:
                try:
                    driver.quit()
                except Exception:
                    pass
