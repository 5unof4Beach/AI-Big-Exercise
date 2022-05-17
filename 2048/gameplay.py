import numpy
import random
from settings import Settings


class Gameplay:
    def __init__(self):
        self.settings = Settings()
        self.grid = [[]]

    def init_grid(self):
        self.grid = numpy.zeros((self.settings.grid_size,
                                 self.settings.grid_size),
                                 dtype=int)

    def next_number(self, k=1):#Hàm này để lấy ngẫu nhiên 2 số 2 hoặc 4 để đặt vào những vị trí có giá trị = 0 trên ma trận
        # lấy tất cả các vị trí có gía trị = 0 trong ma trận
        zeros_pos = list(zip(*numpy.where(self.grid == 0)))

        # lấy ngẫu nhiên k vị trí trong list các vị trí = 0 để đặt 2 giá trị 2 hoặc 4
        for pos in random.sample(zeros_pos, k):
            rand = random.randint(0, 1)
            if rand == 0:
                self.grid[pos] = 4
            else:
                self.grid[pos] = 2

    def move_event(self, key):
        # Hàm này sẽ nhậm tham số là l,r,u,d và được gọi đến khi có sự kiện ấn nút của người dùng
        # sau khi nhận tham số thì hàm sẽ tiến hành xử lí cho giống với logic game 2048
        for i in range(self.settings.grid_size):
            flipped = False
            if key in 'lr':  # nếu nhập vào là l hoặc r thì lấy hàng
                row = self.grid[i, :]
            else:
                row = self.grid[:, i]  # u hoăc d thì lấy cột

            if key in 'rd':  # nếu là r hoặc d thì lật ngược list để có thể tận dụng hàm get num
                flipped = True
                row = row[::-1]

            this_n = self._get_num(row)  # list những số != 0 trong hàng
            # print(this_n)
            new_row = numpy.zeros_like(row)  # tạo một hàng mới chỉ chứa số 0 có kích cỡ giống hàng cũ
            new_row[:len(this_n)] = this_n  # gắn các giá trị != 0 vào mảng mới

            if flipped:
                new_row = new_row[::-1]

            if key in 'lr':
                self.grid[i, :] = new_row
            else:
                self.grid[:, i] = new_row

    # phương thức lấy tập những số khác 0 trong list và xử lý theo cách chơi của 2048
    @staticmethod
    def _get_num(row):
        this_n = row[row != 0]
        res = []
        skip = False
        for i in range(len(this_n)):
            if skip:
                skip = False
                continue
            if i != len(this_n) - 1 and this_n[i] == this_n[i + 1]:  # nếu 2 số liền nhau mà giống nhau thì cộng lại và cho vào mảng mới
                sum = this_n[i] * 2
                res.append(sum)
                skip = True
            else:
                res.append(this_n[i])
        return res

    # Hàm này để test
    def __str__(self):
        return str(self.grid)

    # hàm kiểm tra sau khi bấm nút có thay đổi j ko
    def is_the_same(self, previous_grid):
        if all((self.grid.flatten() == previous_grid.flatten())):
            return True

    # trả về một bản sao trước khi thay dổi của ma trận
    def get_grid(self):
        return self.grid.copy()
