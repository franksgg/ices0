import connector
from fdb import TransactionContext

connection = connector.Connector()


# Function called to initialize your python environment.
# Should return 1 if ok, and 0 if something went wrong.
def ices_init():
    return 1


# Function called to shut down your python enviroment.
# Return 1 if ok, 0 if something went wrong.
def ices_shutdown():
    print('Executing shutdown() function...')
    return 1


# Function called to get the next filename to stream.
# Should return a string.
def ices_get_next():
    connection = connector.Connector()
    dcon = connection.getconnection()
    with TransactionContext(dcon.trans()) as tr:
        cure = tr.cursor()
        cure.execute('select nextpause() from actpos')
        # cure.execute('select first 1 path from tracks')
        d = cure.fetchone()
    return mkmeta(d[0], 'UTF-8')


def mkmeta(song, encoding='ascii'):
    return song.encode(encoding, "ignore")


# This function, if defined, returns the string you'd like used
# as metadata (ie for title streaming) for the current song. You may
# return null to indicate that the file comment should be used.
def ices_get_metadata():
    connection = connector.Connector()
    dcon = connection.getconnection()
    with TransactionContext(dcon.trans()) as tr:
        cure = tr.cursor()
        cure.execute('select actname() from actpos')
        # cure.execute('select first 1 path from tracks')
        d = cure.fetchone()
    return mkmeta(d[0])


if __name__ == '__main__':
    print(ices_get_next())
