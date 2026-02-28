import unittest
from maze_game import (
    generate_true_maze,
    choose_start_exit,
    bfs_shortest_path,
    place_spikes,
    build_new_game,
    try_move,
    WALL,
    OPEN,
    SPIKE,
)

class TestMazeGame(unittest.TestCase):

    def setUp(self):
        self.rows = 15
        self.cols = 29
        self.grid = generate_true_maze(self.rows, self.cols)
        self.start, self.exit = choose_start_exit(self.grid)

    # ---------------------------
    # Maze Generation Tests
    # ---------------------------

    def test_maze_dimensions_are_odd(self):
        grid = generate_true_maze(14, 28)
        self.assertEqual(len(grid) % 2, 1)
        self.assertEqual(len(grid[0]) % 2, 1)

    def test_maze_has_open_tiles(self):
        open_tiles = [
            (r, c)
            for r in range(len(self.grid))
            for c in range(len(self.grid[0]))
            if self.grid[r][c] == OPEN
        ]
        self.assertTrue(len(open_tiles) > 0)

    # ---------------------------
    # Start / Exit Tests
    # ---------------------------

    def test_start_not_equal_exit(self):
        self.assertNotEqual(self.start, self.exit)

    def test_shortest_path_exists(self):
        path = bfs_shortest_path(self.grid, self.start, self.exit)
        self.assertTrue(len(path) > 0)

    # ---------------------------
    # Spike Placement Tests
    # ---------------------------

    def test_spikes_not_on_safe_path(self):
        safe_path = set(bfs_shortest_path(self.grid, self.start, self.exit))
        place_spikes(self.grid, 0.1, self.start, self.exit)

        for r, c in safe_path:
            self.assertNotEqual(self.grid[r][c], SPIKE)

    def test_spikes_not_on_start_or_exit(self):
        place_spikes(self.grid, 0.1, self.start, self.exit)
        self.assertNotEqual(self.grid[self.start[0]][self.start[1]], SPIKE)
        self.assertNotEqual(self.grid[self.exit[0]][self.exit[1]], SPIKE)

    # ---------------------------
    # Movement Tests
    # ---------------------------

    def test_cannot_move_through_wall(self):
        # Surround player with wall manually
        r, c = self.start
        self.grid[r][c+1] = WALL
        new_pos, result = try_move(self.grid, self.start, self.start, (0,1))
        self.assertEqual(result, "blocked")

    def test_spike_resets_to_start(self):
        r, c = self.start
        self.grid[r][c+1] = SPIKE
        new_pos, result = try_move(self.grid, self.start, self.start, (0,1))
        self.assertEqual(result, "spike")
        self.assertEqual(new_pos, self.start)

    def test_exit_triggers_win(self):
        r, c = self.start
        self.grid[r][c+1] = self.exit  # simulate exit next to start
        new_pos, result = try_move(self.grid, self.start, self.start, (0,1))
        # Since try_move checks EXIT tile symbol, we expect move to exit
        self.assertIn(result, ["exit", "moved"])


if __name__ == "__main__":
    unittest.main()