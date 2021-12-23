# The actual database class that we use.
import sqlite3
from cj.data.conn import COL_NOVEL_COVER, COL_NOVEL_ID, COL_NOVEL_LOCATION, COL_NOVEL_TITLE, DB, TABLE_NOVELS
from cj.objects.novel import Novel


class CJDB(DB):
    def __init__(self) -> None:
        super().__init__()

    def get_novels(self) -> list:
        """
        Get all the novels that are in the Databse.

        Returns:
            - The novels.
        """
        novels = self.query(f"SELECT * FROM {TABLE_NOVELS}")

        return novels

    def get_novel(self, novel_id: int=None, novel_title: str=None) -> dict:
        """
        Get a novel based on their id or title.

        Params:
            - novel_id(int): The id of the novel.
            - novel_title(str): The title of the nove.

        Returns:
            - dict or None if one or more are found.
        """
        # TODO: change query for title to a LIKE query
        novel = self.query(f"SELECT * FROM {TABLE_NOVELS} WHERE {COL_NOVEL_ID} = ? OR {COL_NOVEL_TITLE} = ?", (novel_id, novel_title))
        
        # Check if more than one novel was found
        if len(novel) > 1:
            return None

        # Return the novel
        return novel[0]

    def add_novel(self, novel: Novel) -> bool:
        """
        Add a novel to the Database.

        Params:
            - novel(Novel): The novel to add.
        
        Returns:
            - bool True for added false for not added
        """
        # The Query
        query = f"""
        INSERT INTO {TABLE_NOVELS} 
        ({COL_NOVEL_ID}, {COL_NOVEL_TITLE}, {COL_NOVEL_LOCATION}, {COL_NOVEL_COVER}) 
        VALUES (:{COL_NOVEL_ID}, :{COL_NOVEL_TITLE}, :{COL_NOVEL_LOCATION}, :{COL_NOVEL_COVER})
        """
        values = novel.to_json()

        try:
            # Execute the query
            self.execute(query, values)
            return True
        except Exception as e:
            # print("Exception occured while adding novel: {} Exception was:".format(novel), e)
            return False

    def update_novel(self, novel: Novel) -> bool:
        """
        Update a novel.
        """
        query = f"""
        UPDATE {TABLE_NOVELS}
        SET {COL_NOVEL_TITLE} = :{COL_NOVEL_TITLE}, {COL_NOVEL_LOCATION} = :{COL_NOVEL_LOCATION}, {COL_NOVEL_COVER} = :{COL_NOVEL_COVER}
        WHERE {COL_NOVEL_ID} = :{COL_NOVEL_ID}
        """
        values = novel.to_json()

        try:
            # Execute the query
            self.execute(query, values)
            return True
        except Exception as e:
            # print("Exception occured while updating novel: {} Exception was:".format(novel), e)
            return False