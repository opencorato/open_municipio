from data_import.lib import Ballot, Sitting, Vote, BaseVotationReader
from data_import.senigallia import conf

import re, os

class MdbVotationReader(BaseVotationReader):
    """
    Parse votation-related data from a set of MDB files. 
    """
    def get_data_source(self):
        """
        In this case, the data source is a filesystem directory containing MDB files
        """
        conf.MDB_ROOT_DIR
        
    def _is_valid_votation_mdb(self, fname):
        """
        Takes a file name ``fname``: if that string is a valid filename for a MDB file 
        containing votation data for a given sitting of the City Council, returns ``True``; 
        otherwise, returns ``False``.
        """
        pattern = re.compile(conf.MDB_FILENAME_PATTERN)
        if pattern.match(fname):
            return True
        else:
            return False
        
    def _get_sitting_id_from_mdb(self, fname):
        """
        Takes the name of a MDB file containing votation data for a given sitting 
        of the City Council; returns the corresponding sitting ID, as a string.
        """
        pattern = re.compile(conf.MDB_FILENAME_PATTERN)
        m = pattern.match(fname)
        return m.group('sitting_id')
        
    def _mdb_to_sqlite(self, mdb_fpath, sqlite_fpath):
        """
        Converts MDB files containing votation data to SQLite databases.
        
        Takes a path to a MDB file, ``mdb_fpath`` and creates an equivalente 
        SQLite DB file located at ``sqlite_fpath``.        
        """
        raise NotImplementedError
    
    def _get_sitting_seq_n(self, sitting_id):
        """
        Takes the internal ID for a sitting (as set by the ballot management system)
        and returns the sequential number since the beginning of the current year. 
        """
        # TODO: replace this dummy implementation
        return sitting_id
        
    def setup(self):
        # if the root dir holding SQLite files doesn't exist yet, create it
        if not os.path.exists(conf.SQLITE_ROOT_DIR):
            os.mkdir(conf.SQLITE_ROOT_DIR)
        # loop over (valid) MDB files and convert them to SQLite DBs
        for fname in os.listdir(conf.MDB_ROOT_DIR):
            # sanity check
            if self._is_valid_votation_mdb(fname):
                sitting_id = self._get_sitting_id_from_mdb(fname)
                # create a SQLite DB containing the same votation data as the MDB file 
                mdb_fpath = os.path.join(conf.MDB_ROOT_DIR, fname)
                sqlite_fpath = os.path.join(conf.SQLITE_ROOT_DIR, sitting_id + '.sqlite')
                self._mdb_to_sqlite(mdb_fpath, sqlite_fpath)
        
        def get_sittings(self):
            sittings = []
            # loop over the SQLite DBs containing votation data
            for fname in os.listdir(conf.SQLITE_ROOT_DIR):
                # sitting IDs are encoded within DB filenames
                sitting_id = fname.rstrip('.sqlite')
                sitting = Sitting()
                sitting.seq_n = self._get_sitting_seq_n(sitting_id)
                # TODO: retrieve sitting's ``call`` and ``date`` attributes, and set them
                sittings.append(sitting)  