from pgzero.actor import Actor

from static import HEIGHT, WIDTH, BASE_HEIGHT, BASE_WIDTH
from utils import scale_to


class BranchProvider:
    def __init__(self, screen):
        self.branch_count = 10
        self.screen = screen
        self.screen_width = self.screen.surface.get_size()[0]
        self.screen_height = self.screen.surface.get_size()[1]
        self.left_branches = [self.create_branch() for _ in range(self.branch_count)]
        self.right_branches = [self.create_branch(left=False) for _ in range(self.branch_count)]

        scale_to(self.all_branches(), (BASE_WIDTH, BASE_HEIGHT), (WIDTH, HEIGHT), change_pos=False)

    def all_branches(self):
        return self.left_branches + self.right_branches

    def create_branch(self, left=True):
        branch_scale_left = 369 / 800
        branch_scale_right = 432 / 800
        branch_left_unused = Actor('konar_lewy')
        if left:
            branch = Actor('konar_lewy', pos=(branch_scale_left * WIDTH, 100), anchor=(branch_left_unused.width, 0))
        else:
            branch = Actor('konar_prawy', pos=(branch_scale_right * WIDTH, 100), anchor=(0, 0))
        return branch

    def branches_to_draw(self):
        branches = []
        for branch in self.all_branches():
            if 0 <= branch.y <= self.screen_height:
                branches.append(branch)
        return branches
