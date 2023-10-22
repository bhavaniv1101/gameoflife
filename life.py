# -*- coding: utf-8 -*-
"""
Created on Thu May 27 16:50:41 2021

@author: bhava
"""


import matplotlib.pyplot as plt


class Grid:
    """
    Represent Game of Life grid.

    Size n by n and wrapped around at the edges.

    Parameters
    ----------
    size : int
        Number of rows or columns in the grid.
    """

    def __init__(self, size):
        """
        Initialize object.
        """
        self.size = size
        self.on_cells = set()

    def turn_on(self, cells):
        """
        Turn on specified cells.

        Parameters
        ----------
        cells : iterable of tuples
            Iterable of tuples (r, c) where r and c represent the row and
            column indices of a cell to turn on. r and c should be in
            range(self.size).
        """
        self.on_cells = self.on_cells.union(cells)

    def turn_off(self, cells):
        """
        Turn off specified cells.

        Parameters
        ----------
        cells : iterable of tuples
            Iterable of tuples (r, c) where r and c represent the row and
            column indices of a cell to turn off. r and c should be in
            range(self.size).
        """
        self.on_cells = self.on_cells.difference(cells)

    def neighbours(self, cell):
        """
        Return neighbours of given cell.

        Parameters
        ----------
        cell : tuple
            Tuple (r, c) where r and c represent the row and column indices of
            a cell. r and c should be in range(self.size).

        Returns
        -------
        nbrs : set of tuples
            Set of tuples (r, c) where r and c represent the row and column
            indices of neighbours of a given cell.
        """
        nbrs = set()
        r, c = cell
        # We need to take the remainder to wrap around at the edges.
        for i_row in ((r - 1) % self.size, r, (r + 1) % self.size):
            for i_col in ((c - 1) % self.size, c, (c + 1) % self.size):
                if (i_row, i_col) == (r, c):
                    continue
                nbrs.add((i_row, i_col))
        return nbrs

    def on_neighbours(self, cell):
        """
        Return on cells neighbouring given cell.

        Parameters
        ----------
        cell : tuple
            Tuple (r, c) where r and c represent the row and column indices of
            a cell. r and c should be in range(self.size).

        Returns
        -------
        on_nbrs : set of tuples
            Set of tuples (r, c) where r and c represent the row and column
            indices of on neighbours of a given cell.
        """
        return self.on_cells.intersection(self.neighbours(cell))

    def update(self):
        """
        Update grid based on rules of Game of Life.
        """
        # Keep track of which cells will be on after updating.
        new_on_cells = set()
        # We will find all off neighbours of on cells. Only off cells that
        # neighbour on cells can turn on.
        off_nbrs_of_on_cells = set()
        # Check which on cells will remain on.
        for cell in self.on_cells:
            nbrs = self.neighbours(cell)
            on_nbrs = nbrs.intersection(self.on_cells)
            if len(on_nbrs) in (2, 3):
                new_on_cells.add(cell)
            off_nbrs = nbrs.difference(on_nbrs)
            off_nbrs_of_on_cells = off_nbrs_of_on_cells.union(off_nbrs)
        # Check which off cells will turn on.
        for cell in off_nbrs_of_on_cells:
            on_nbrs = self.on_neighbours(cell)
            if len(on_nbrs) == 3:
                new_on_cells.add(cell)
        self.on_cells = new_on_cells

    def display(
            self,
            n_updates: int = 1000,
            update_period_s: float = 0.1
    ) -> None:
        """
        Display states of all cells.

        Parameters
        ----------
        n_updates : int, optional
            Number of updates to perform.
        update_period_s : float, optional
            Interval (s) between successive updates.
        """
        fig, axs = plt.subplots(figsize=(14, 14))
        self._display(axs, title='Initial state')
        for i_u in range(n_updates):
            self.update()
            self._display(axs, title=f'State after {1 + i_u} updates')
            plt.pause(update_period_s)

    def _display(
            self,
            axs,
            title: str = ''
    ) -> None:
        """
        Display states of all cells on given axes.
        """
        # Make list of lists with 0-1 elements, with 1 indicating "on" cells.
        arr = [[0 for _ in range(self.size)] for _ in range(self.size)]
        for i_r, i_c in self.on_cells:
            arr[i_r][i_c] = 1
        # Display above list of lists as an image on given axes.
        axs.cla()  # Clear the figure
        axs.axis('off')  # Turn off axes
        axs.set_title(title)
        axs.imshow(arr)  # Plot the figure


def main():
    """
    Main function.
    """
    size = 200
    on_cells = [(size // 2 + r, size // 2 + c)
                for r, c in [(0, 0), (1, 0), (1, 1), (1, 2), (2, 1)]]
    grid = Grid(size)
    grid.turn_on(on_cells)
    print('Initial state:', grid.on_cells)
    # Run simulation.
    grid.display(n_updates=10000, update_period_s=0.1)


if __name__ == "__main__":
    main()
