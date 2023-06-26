from random import randint


def create(width, height, number_of_bombs, blocks, initial):
    for i in range(0, height + 2):
        blocks.append(list())
        for j in range(0, width + 2):
            if (i,j)==initial:
                blocks[i].append(block(j, i, False,True))
            else:
                blocks[i].append(block(j, i, False,False))
    bombs = 0
    while bombs != number_of_bombs:
        x = randint(1, width)
        y = randint(1, height)
        can_bomb=True
        for i in range(y-1,y+2):
            for j in range(x-1,x+2):
                if initial==(i,j):
                    can_bomb=False
                    break
        if can_bomb and blocks[y][x].make_it_bomb(blocks):
            bombs += 1

    blocks[initial[0]][initial[1]].revealed=False
    for y in range(1, height + 1):
        for x in range(1, width + 1):
            blocks[y][x].calculate_bombs(blocks)

    for i in (0,-1):
        for j in range(len(blocks[i])):
            blocks[i][j].is_real=False
    for i in range(len(blocks)):
        for j in(0,-1):
            blocks[i][j].is_real=False


    """blocks=blocks[1:-1]
    for i in range(height):
        blocks[i]=blocks[i][1:-1]"""

    return blocks


class block:
    def __init__(self, x, y, bomb,revealed):
        self.x = x
        self.y = y
        self.bomb = bomb
        self.number = None
        self.revealed= revealed
        self.is_real=True
        self.is_flagged=False 
        self.finished=False
    def is_bomb(self):
        return self.bomb

    def bombs_around(self):
        return self.number
    
    def is_revealed(self):
        return self.revealed
    
    def make_it_bomb(self, blocks):
        if self.is_bomb() or self.is_revealed():
            return False
        can_be_bomb = False
        for y in range(self.y - 1, self.y + 2):
            for x in range(self.x - 1, self.x + 2):
                if not blocks[y][x].is_bomb():
                    can_be_bomb = True
                    break
        if can_be_bomb:
            self.bomb = True
            return True
        else:
            return False

    def calculate_bombs(self, blocks):
        if self.is_bomb():
            return False
        self.number = 0
        for y in range(self.y - 1, self.y + 2):
            for x in range(self.x - 1, self.x + 2):
                if blocks[y][x].is_bomb():
                    self.number += 1

    def reveal_first(self,blocks):
        if self.is_revealed() or self.is_flagged:
            return None
        if self.is_bomb():
            return False
        else:
            return self.reveal_blocks(blocks)
        
    
    def reveal_blocks(self,blocks):
        if self.is_bomb() or not self.is_real or self.is_flagged:
            return []
        self.revealed=True
        if self.number!=0:
            return [(self.number,self.x,self.y)]
        alist=[(self.number,self.x,self.y)]
        for y in range(self.y-1,self.y+2):
            for x in range(self.x-1,self.x+2):
                if not blocks[y][x].is_revealed():
                    for i in blocks[y][x].reveal_blocks(blocks):
                        alist.append(i)
        return alist
    def flag_it(self):
        if not self.is_revealed():
            self.is_flagged= not self.is_flagged
            return True,self.is_flagged
        return False,None
    
    def auto_reveal(self,blocks):
        if not self.is_revealed() or self.is_flagged:
            return None
        no=0
        for y in range(self.y-1,self.y+2):
            for x in range(self.x-1,self.x+2):
                if blocks[y][x].is_flagged:
                    no+=1
        if no!=self.number:
            return None #TO DO: Later
        alist=[]

        for y in range(self.y-1,self.y+2):
            for x in range(self.x-1,self.x+2):
                if not blocks[y][x].is_flagged:
                    temp=blocks[y][x].reveal_first(blocks)
                    if temp==False:
                        return False
                    if temp is not None:
                        if False in temp:
                            return False
                        for i in temp:
                            alist.append(i)
        return alist
    

def main():
    blocks = []
    blocks = create(9, 9, 10, blocks ,(7,7))
    for i in range(1, 10):
        for j in range(1, 10):
            if blocks[i][j].is_bomb():
                print("*", end=" ")
            else:
                print(blocks[i][j].bombs_around(), end=" ")
        print()


"""if __name__ == "__main__":
    main()"""
