# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import openpyxl
import pymysql

class dbpline:
    def open_spider(self, spider):
        self.conn=pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            passwd='123456',
            db='spider',
            charset='utf8mb4'
        )
        self.cursor=self.conn.cursor()
        self.cursor.execute('truncate table top_movie;')
        self.conn.commit()
        self.data=[]
    def process_item(self, item, spider):
        self.data.append((item["title"], item["rank"], item["subject"]))
        if len(self.data)==100:
            self._write_to_db()
            self.data.clear()
        return item
    def close_spider(self, spider):
        if len(self.data)>0:
            self._write_to_db()
        self.conn.close()
    def _write_to_db(self):
        self.cursor.executemany("insert into top_movie(title,rating,subject) values (%s,%s,%s)",
                                self.data)
        self.conn.commit()




class Spider2026Pipeline:
    def open_spider(self, spider):
        # 爬虫启动只执行一次，创建全新工作簿
        self.wb = openpyxl.Workbook()
        # 删除默认空白Sheet，只保留自己创建的
        self.wb.remove(self.wb.active)
        self.ws = self.wb.create_sheet("top250")
        # 写入表头
        self.ws.append(["标题", "评分", "主题"])

    def process_item(self, item, spider):
        # 打印日志，确认数据进管道（关键调试）
        print("当前写入数据：", item["title"], item["rank"], item["subject"])
        row_data = [
            item.get("title", "空"),
            item.get("rank", "空"),
            item.get("subject", "空")
        ]
        self.ws.append(row_data)
        return item
    def close_spider(self, spider):
        # 绝对路径保存到桌面，杜绝路径找不到
        save_path = r"C:\Users\王立硕\Desktop\电影数据3.xlsx"
        self.wb.save(save_path)
        print("文件已保存至：", save_path)