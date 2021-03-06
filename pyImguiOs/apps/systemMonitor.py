from pyImguiOs.core import Window
import imgui
import psutil

class SystemMonitor(Window):
    def __init__(self):
        self.attrs=['pid','name','cpu_percent','memory_percent','username',]
        self.tickrate=1
        self.sortKey='cpu_percent'
        self.reverseSort=True
        super().__init__()
        self.update(0)

    def update(self,dt):
        self.processList = list(psutil.process_iter(attrs=self.attrs))
        self.processList.sort(key=lambda x: x.info[self.sortKey],reverse=self.reverseSort)

    def render_row(self, process):
        imgui.begin_group()
        for key in self.attrs:
            imgui.text(str(process.info[key]))
            imgui.next_column()
        imgui.end_group()
        if imgui.is_item_clicked():
            pass

    def render_header(self, item):
        if item == self.sortKey:
            imgui.text("* "+item)
        else:
            imgui.text(item)
        if imgui.is_item_clicked():
            if item == self.sortKey:
                self.reverseSort = not self.reverseSort
            self.sortKey=item
        imgui.next_column()

    def render(self):
        imgui.columns(len(self.attrs), 'alertList')
        list(map(self.render_header,self.attrs))
        imgui.separator()
        list(map(self.render_row,self.processList))
        imgui.columns(1)

