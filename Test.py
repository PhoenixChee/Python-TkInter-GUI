def main(self):
    root = Tk()
    frame=Frame(root)
    frame.grid(row=0, column=0)

    self.btn = [[0 for x in xrange(20)] for x in xrange(60)]
    for x in range(60):
        for y in range(20):
            self.btn[x][y] = Button(frame, command=lambda x=x, y=y: self.color_change(x, y))
            self.btn[x][y].grid(column=x, row=y)

    root.mainloop()

def color_change(self,x,y):
    self.btn[x][y].config(bg="red")
    print(x, y)