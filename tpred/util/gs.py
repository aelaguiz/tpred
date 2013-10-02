import datetime
import gdata.spreadsheet.service
import os

email = os.environ['GOOGLE_USERNAME']
password = os.environ['GOOGLE_PASSWORD']
weight = '180'


def clear_spreadsheet(client, spreadsheet_key, ws_key):
    query = gdata.spreadsheet.service.CellQuery()
    query.min_row = '2'

    # Pull just those cells
    no_headers = client.GetCellsFeed(spreadsheet_key, ws_key, query=query)

    batch_request = gdata.spreadsheet.SpreadsheetsCellsFeed()

    # Iterate through every cell in the CellsFeed, replacing each one with ''
    # Note that this does not make any calls yet - it all happens locally
    for i, entry in enumerate(no_headers.entry):
        entry.cell.inputValue = ''
        batch_request.AddUpdate(no_headers.entry[i])

    # Now send the entire batchRequest as a single HTTP request
    updated = client.ExecuteBatch(batch_request, no_headers.GetBatchLink().href)

def write_rows(spreadsheet_key, header, rows):
    spr_client = gdata.spreadsheet.service.SpreadsheetsService()
    spr_client.email = email
    spr_client.password = password
    spr_client.source = 'Example Spreadsheet Writing Application'
    spr_client.ProgrammaticLogin()

    #feed = spr_client.GetSpreadsheetsFeed()
    #print feed

    #print feed.get(0)

    ws_key = 'od6'

    #print spr_client.GetWorksheetsFeed(key=spreadsheet_key).entry[0].id.text

    #lfeed = spr_client.GetListFeed(key=spreadsheet_key,wksht_id=ws_key)
    #print lfeed.entry[0].custom

    #cells = spr_client.GetCellsFeed(spreadsheet_key, ws_key)

    clear_spreadsheet(spr_client, spreadsheet_key, ws_key)


    for row in rows:
        d = {}
        for c, r in zip(header, row):
            c = c.lower()
            c = c.replace(" ", "")
            d[c] = r

        print d, spreadsheet_key, ws_key
        spr_client.InsertRow(d, spreadsheet_key, ws_key)


    ### Prepare the dictionary to write
    ##dict = {}
    ##dict['date'] = time.strftime('%m/%d/%Y')
    ##dict['time'] = time.strftime('%H:%M:%S')
    ##dict['weight'] = weight
    ##print dict

    ##entry = spr_client.InsertRow(dict, spreadsheet_key, worksheet_id)
    ##if isinstance(entry, gdata.spreadsheet.SpreadsheetsList):
        ##print "Insert row succeeded."
    ##else:
        ##print "Insert row failed."
