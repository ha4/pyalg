�������� ��������� [https://habr.com/ru/post/176671/]
==================

���������: �� ������������, ��� ����� ����� ������ ����� ������� �����, � ����� ������ � ������.

1. �������� ������ ������. �� ���� ������ �� ����� �������� ������ �� ������ ���������.
2. ��������� �������, �� �������� � ���������, ���� ���������� ���������.
3. �������� ������ �������, �������� ����� �������:
   * �������� ������ ��������� ������� ��� ���
     1. ���� ������� ������ � ������ ������ ����������� ������ ���������, �� �������� ������� ����� ���� (��� �������������� ������������)
     2. ���� �� ������ �� ��������� �������, �� ���������� ��� ��������� � ������� ��������� ������� ������ � ������ ������.
4. �������� ������� �����, �������� ����� �������:
   * �������� ������ ��������� ������� ��� ���. ��������� ��� ������ ��������� ����� ���� �� ���� ������ ��� ������ ������� (��� �������������� ������������ ��������)
     1. ���� ������ � ����� ��������� ����, �� �� ���������� ������� �����
     2. ���� ������ ���� � ����� ��������� ��� ������ �������, �� �� ���������� ������ �������
5. ������, ������ �� �� ������ ��������� ������ ��� ������ ��������� ��������
   1. ���� �� ������ �������� ��� ���� ������, ��:
      1. �������� ������� ������
      2. ������� ��� ������ �������
      3. ������� ������ � ������ �������� �� �� ���������
      4. ������� ��� ������ �������
      5. ����������� � ���� 2
    2. ���� �� ������ ��������� ��������, ��:
      1. �������� ������ ������� � ������ ������
      2. �������� ����� �������:
         * ���� ������� ������ � ������ ������ ����� ������ ��������, ��:
           1. ������� ������ �������
           2. ���������� ��������� ������� ������ � ������ ������
           3. �������� ����������� ������

The Algorithm [http://www.neocomputer.org/projects/eller.html]
=============
Note: Assume that there all left-most cells have a left-wall and all right-most cells have a right wall.

1. Create the first row. No cells will be members of any set

2. Join any cells not members of a set to their own unique set

3. Create right-walls, moving from left to right:
   A. Randomly decide to add a wall or not
      * If the current cell and the cell to the right are members of the same set, always create a wall between them. (This prevents loops)
      * If you decide not to add a wall, union the sets to which the current cell and the cell to the right are members.

4. Create bottom-walls, moving from left to right:
   A. Randomly decide to add a wall or not. Make sure that each set has at least one cell without a bottom-wall (This prevents isolations)
      * If a cell is the only member of its set, do not create a bottom-wall
      * If a cell is the only member of its set without a bottom-wall, do not create a bottom-wall

5. Decide to keep adding rows, or stop and complete the maze
   A. If you decide to add another row:
      a. Output the current row
      b. Remove all right walls
      c. Remove cells with a bottom-wall from their set
      d. Remove all bottom walls
      e. Continue from Step 2
   B. If you decide to complete the maze
      a. Add a bottom wall to every cell
      b. Moving from left to right:
         * If the current cell and the cell to the right are members of a different set:
           i. Remove the right wall
           ii. Union the sets to which the current cell and cell to the right are members.
           iii. Output the final row

Eller's Algorithm [http://weblog.jamisbuck.org/2010/12/29/maze-generation-eller-s-algorithm]
=================
1. Initialize the cells of the first row to each exist in their own set.
2. Now, randomly join adjacent cells, but only if they are not in the same set. When joining adjacent cells, merge the cells of both sets into a single set, indicating that all cells in both sets are now connected (there is a path that connects any two cells in the set).
3. For each set, randomly create vertical connections downward to the next row. Each remaining set must have at least one vertical connection. The cells in the next row thus connected must share the set of the cell above them.
4. Flesh out the next row by putting any remaining cells into their own sets.
5. Repeat until the last row is reached.
6. For the last row, join all adjacent cells that do not share a set, and omit the vertical connections, and you�re done!
