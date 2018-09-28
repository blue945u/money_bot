# encoding: utf-8

import re

class CianCianBot:
    commands = {
            "HELP": ("說明", "幫幫"),
            "SUMMARY": (),  # [TODO 8]
            "RECENT_RECORDS": (),  # [TODO 10]
            "INTERNAL_TEST": ("測試帳號",),
            }

    def __init__(self, data_manager):
        self.data_manager = data_manager

    def get_help(self):
        """
        Returns a string to help new users.
        """
        # [TODO 1]
        help_msg = "讓我教你怎麼用：\n 名子欠名子$金額 說明\n（ex:小明欠小花$100 晚餐）"



        return help_msg

    @staticmethod
    def _get_presenting_order(person1, person2, balance_number):
        """
        Sort the presenting order of the two people.

        Returns:
            (borrower, owner, money)
            Where `money` should be positive.

        Purpose:
            當得到 ('A', 'B', -300) 這樣的 summary record，
            代表「A欠B -300元」，但我們必須輸出「B欠A 300元」
            這個小 method 就是為了解決此 sorting 問題

        e.g. 1
        [Input]  ('A', 'B', -300)
        [Output] ('B', 'A', 300)

        e.g. 2
        [Input]  ('X', 'Y', 300)
        [Output] ('X', 'Y', 300)
        """

        # [TODO 6]
        # case 1 -「B欠A $xx元」, xx > 0


        # case 2 -「A欠B $xx元」, xx > 0



        return ('person??', 'person??', 'positive_balance_number')

    def get_all_summary(self, unique_id):
        """
        Get all people pairs' balance numbers. And output the summary results.
        """
        # 1. Get balance records from database [TODO 8]
        #    Hint: call `self.data_manager.get_all_summary(...)`



        # 2. Format outputs
        #    "目前 熊大欠茜茜 5566元，茜茜欠大雄 1234元，大雄欠熊大 888元。"
        strs = []
        for person1, person2, balance_number in balance_records:
            strs.append("%s欠%s %d元" % self._get_presenting_order(person1, person2, balance_number))
        main_sentences = "，".join(strs)
        if not main_sentences:
            return "目前沒有任何記錄哦！！"
        else:
            return "目前 " + main_sentences + "。"

    def get_recent_records(self, unique_id):
        try:
            records = self.data_manager.get_recent_records(unique_id)
        except Exception:
            return "抱歉，擷取資料時出現了錯誤。"

        if not records:
            return "目前沒有任何記錄哦！"

        # Formating records to strings. [TODO 12]
        result = str(records)

        # ------ Sample ------
        # 2016/1/3 14:23
        # 熊大欠茜茜 300元 午餐吃了超好吃的雅室牛排
        #
        # 2016/1/4 19:23
        # 熊大欠茜茜 1490元 神魔卡包
        # --------------------

        return result

    def process_borrow_statement(self, msg, unique_id):
        """
        If `msg` is not a borrow statement, return None.
        Otherwise, return the result of writing this borrow record.

        Returns:
            A string, that shows
                1. The result of writing borrow record.
                2. Current balance number between the two people mentioned.

            Or when encountering an error, returns a string indicating the error.
        """
        match_obj = re.match(".+欠.+\$.+[0-9]", msg)
        if not match_obj:
            return None

        # 1. Extract `borrower`, `owner`, `money`, `note` from `msg`. [TODO 3]
        tmp_list = msg.split("欠")
        borrower = tmp_list[0]
        tmp_list = tmp_list[1].split("$")
        owner = tmp_list[0]
        tmp_list = tmp_list[1].split(" ")
        if len(tmp_list) > 1:
            money = tmp_list[0]
            note = tmp_list[1]
        else:
            money = tmp_list[0]
            note = None

        # 2. Write the record (`unique_id`, `borrower`, `owner`, `money`, `note`) to DataManager.
        #    Hint: call `self.data_manager.write(...)`, mind the return values of this method.
        summery = self.data_manager.write(unique_id, borrower, owner, money, note)
        resopn_string = "新增紀錄 "+borrower+" 欠 "+owner+" "+money+"元。\n目前 "+summery[0]+"欠"+summery[1]+str(summery[2])+"元。"
        #    also returns the latest balance_number.
        #    Hint: Use `self._get_presenting_order(...)` [TODO 6]

        return resopn_string

    def respond(self, msg, unique_id):
        """
        The main responding mechanism of CianCianBot.

        Args:
            msg: User's message.
            unique_id: The chatting window id of that user.

        Returns:
            A string.
        """

        # 「說明、幫幫」
        if msg in self.commands["HELP"]:
            return self.get_help()

        # 「結帳」Use `self.get_all_summary(...)` [TODO 8]


        # 「最近帳單」Use `self.get_recent_records(...)` [TODO 10]


        # 「測試帳號」(Only for testing)
        elif msg in self.commands["INTERNAL_TEST"]:
            return unique_id

        else:
            result = self.process_borrow_statement(msg, unique_id)
            if not result:
                return "我聽不懂你在說什麼！"
            else:
                # 「A欠B $$$元」
                return result


if __name__ == "__main__":

    ##########################################
    # A function for local test.
    ##########################################

    def local_test(msg, bot):
        if msg:
            bot_response = bot.respond(msg, "fake_unique_id_for_testing")
            print("-" * 30)
            print("  [User]")
            print(msg)
            print("  [Bot]")
            print(bot_response)
        else:
            # If `msg` is None, print newlines, forming a paragraph.
            print("\n\n")

    ##########################################
    # Basic testcases.
    ##########################################

    testcases = [
            "說明",
            "茜茜欠熊大$300",
            "茜茜欠熊大$300 晚餐",
            "結帳",
            "最近帳單",
            "說明",
            ]

    from DataManager import DataManager
    data_manager = DataManager()
    cian_cian = CianCianBot(data_manager)

    for user_input in testcases:
        local_test(user_input, cian_cian)
