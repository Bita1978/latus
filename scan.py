import core.db
import core.metadatapath
import core.util
import core.larg

if __name__ == "__main__":
    larg_parser = core.larg.LatusArg("Scans a folder/directory and updates the metadata database")
    args = larg_parser.parse()

    db = core.db.DB(core.metadatapath.MetadataPath(args.metadata))
    db.scan(args.path)
