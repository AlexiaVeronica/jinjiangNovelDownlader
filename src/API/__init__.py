import template
from lib import GET, CheckJsonAndAddModel
from rich import print
from . import UrlConstant


@CheckJsonAndAddModel(template.BookInfo)
@GET(UrlConstant.NOVEL_INFO)
def novel_basic_info(response: dict):  # get book information by novel_id
    return response, UrlConstant.WEB_HOST + UrlConstant.NOVEL_INFO


@GET(UrlConstant.SEARCH_INFO)
def search_home_page(response: dict) -> [dict, None]:  # search book by keyword
    if response.get("code") == '200':
        return response.get("data")
    else:
        print("search failed:", response.get("message"))


@GET("getUserCenter")
def get_user_center(response: dict) -> template.UserCenter:
    user_center = template.UserCenter(**response)
    if not user_center.message:
        return user_center
    print("[err]get user info failed:", user_center.message)


@GET("getAppUserinfo")
def get_user_info(response: dict) -> template.UserInfo:
    user_info = template.UserInfo(**response)
    if not user_info.message:
        return user_info
    print("get user info failed:", user_info.message)


@GET("search")
def search_book(response: dict):  # search book by keyword
    novel_info_list = []
    if response.get("items"):
        for index, novel_info in enumerate(response.get("items")):
            novel_info_list.append(template.SearchInfo(**novel_info))
    else:
        if response.get("message") == "没有更多小说了！":
            return response.get("message")
        else:
            print("search failed:", response.get("message"))

    return novel_info_list


@GET(UrlConstant.CHAPTER_LIST)
def get_chapter_list(response):  # get chapter list by novel_id
    if response.get("message"):
        print("get chapter list failed, please try again.", response.get("message"))
    else:
        return response['chapterlist']


@GET("chapterContent")
def get_chapter_vip_content(response) -> dict:
    try:
        return response
    except Exception as e:
        print(e)


@GET(UrlConstant.CONTENT)
def get_chapter_free_content(response) -> dict:
    try:
        return response
    except Exception as e:
        print(e)
