def suggest_vendor(console, splits):

    matching_vendors = console.dm.get_matching_vendors(splits[console.bl_index].vendor)

    if len(matching_vendors) == 0:
        input('No autocomplete')
        return

    input("MATCHES: " + str(matching_vendors))
