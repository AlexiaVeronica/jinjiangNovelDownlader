import jinjiangAPI
import catalogue
from instance import *


class Book:
    def __init__(self, book_info: dict):
        self.book_info = book_info
        self.book_id = book_info["novelId"]
        self.book_name = book_info["novelName"]
        self.book_author = book_info["authorName"]
        self.book_cover = book_info["originalCover"]
        self.book_intro = book_info["novelIntroShort"]
        self.book_class = book_info["novelClass"]
        self.book_tags = book_info["novelTags"]
        self.book_tags_id = book_info["novelTagsId"]
        self.book_size = book_info["novelSize"]
        self.book_chapter_count = book_info["novelChapterCount"]
        self.book_score = book_info["novelScore"]
        self.book_is_lock = book_info["islock"]
        self.book_is_vip = book_info["isVip"]
        self.book_is_package = book_info["isPackage"]
        self.book_is_sign = book_info["isSign"]
        self.vip_chapterid = book_info["vipChapterid"]
        self.book_main_view = book_info["mainview"]
        self.book_code_url = book_info["codeUrl"]
        self.book_review_score = book_info["novelReviewScore"]
        self.book_author_say_rule = book_info["authorsayrule"]
        self.series = book_info["series"]
        self.protagonist = book_info["protagonist"]
        self.costar = book_info["costar"]
        self.other = book_info["other"]

    def __str__(self) -> str:
        show_book_info = "book_name:{}".format(self.book_name)
        show_book_info += "\nbook_author:{}".format(self.book_author)
        show_book_info += "\nbook_cover:{}".format(self.book_cover)
        show_book_info += "\nbook_intro:{}".format(self.book_intro)
        show_book_info += "\nbook_class:{}".format(self.book_class)
        show_book_info += "\nbook_tags:{}".format(self.book_tags)
        show_book_info += "\nbook_tags_id:{}".format(self.book_tags_id)
        show_book_info += "\nbook_size:{}".format(self.book_size)
        show_book_info += "\nbook_chapter_count:{}".format(self.book_chapter_count)
        show_book_info += "\nbook_score:{}".format(self.book_score)
        show_book_info += "\nbook_is_lock:{}".format(self.book_is_lock)
        print(show_book_info)
        return show_book_info

    def get_catalogue(self):
        response = jinjiangAPI.Chapter.chapter_list(self.book_id)['chapterlist']
        for index, chapter in enumerate(response):
            chapter_info = catalogue.Chapter(chapter_info=chapter, index=index)
            content_info = jinjiangAPI.Chapter.chapter_content(
                novel_id=self.book_id,
                chapter_id=chapter_info.chapter_id,
                vip_chapter=chapter_info.is_vip
            )
            if chapter_info.original_price > 0 and content_info.get("message") is not None:
                print("the chapter {} is vip, skip".format(chapter_info.chapter_name))
                continue
            content_info = catalogue.Content(content_info)
            self.save_content(
                chapter_index=chapter_info.index,
                chapter_id=chapter_info.chapter_id,
                chapter_title=content_info.chapter_name,
                content=content_info.content
            )

    def test_file(self, file_path: str):
        return os.path.exists(file_path)

    def save_content(self, chapter_index: int, chapter_id: str, chapter_title: str, content: str):
        if not self.test_file(os.path.join(Vars.config_text, chapter_id + ".txt")):
            content_text = f"第 {chapter_index} 章" + chapter_title + "\n" + content.replace("&lt;br&gt;&lt;br&gt;", "\n")
            TextFile.write(text_path=os.path.join(Vars.config_text, chapter_id + ".txt"), text_content=content_text)
        else:
            print("the file is exist, skip")

    def download_cover(self):
        pass

    def mkdir_content_file(self):
        Vars.config_text = os.path.join("configs", self.book_name)
        Vars.out_text_file = os.path.join("downloads", self.book_name)
        if not os.path.exists(Vars.config_text):
            os.makedirs(Vars.config_text)
        if not os.path.exists(Vars.out_text_file):
            os.makedirs(Vars.out_text_file)