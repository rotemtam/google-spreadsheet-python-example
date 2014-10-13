import gdata.spreadsheets.client
import gdata.gauth
import gdata.spreadsheets.data
import string

def checkConfig(cfg):
	keys = ['client_id','client_secret','access_token','refresh_token','spreadsheet','worksheet']
	for key in keys:
		if not cfg.get("gdata", key):
			raise Error, "did not find key '%s' in config file." % key

def generateClient(cfg):
    ' generate authenticated spreadsheet '
    token = gdata.gauth.OAuth2Token(client_id=cfg.get("gdata","client_id"),
                                    client_secret=cfg.get("gdata","client_id"),
                                    scope='https://spreadsheets.google.com/feeds/',
                                    user_agent='Gdata test export',
                                    access_token=cfg.get("gdata","access_token"),
                                    refresh_token=cfg.get("gdata","refresh_token"))

    spr_client = gdata.spreadsheets.client.SpreadsheetsClient()
    token.authorize(spr_client)

    return spr_client


def clearData(spr_client,key, worksheet_id, min_row='2'):
    'clear all data under under row 2 (leave room for header row to be unchanged)'
    q = gdata.spreadsheets.client.CellQuery()
    q.min_row = min_row
    cells = spr_client.get_cells(key, worksheet_id, query=q)
    batch = gdata.spreadsheets.data.BuildBatchCellsUpdate(key,worksheet_id)
    for cell in cells.entry:
        cell.cell.input_value = ''
        batch.add_batch_entry(cell, cell.id.text, batch_id_string=cell.title.text, operation_string='update')
    spr_client.batch(batch, force=True)

def writeData(spr_client, key, worksheet_id, data, start_row):
    'write results to spreadsheet as single batch'
    end_letter = string.uppercase[ len(data[0]) - 1 ]

    range = "A%d:%s%d" % (start_row, end_letter, start_row + len(data) - 1)

    cellq = gdata.spreadsheets.client.CellQuery(range=range, return_empty='true')
    cells = spr_client.GetCells(key, worksheet_id, q=cellq)

    objData = gdata.spreadsheets.data
    batch = objData.BuildBatchCellsUpdate(key, worksheet_id)

    for cell in cells.entry:
        row_val = start_row - int(cell.cell.row)
        col_val = int(cell.cell.col) - 1
        val = data[row_val][col_val].replace("\"", "")
        cell.cell.input_value = val
        batch.add_batch_entry(cell, cell.id.text, batch_id_string=cell.title.text, operation_string='update')

    spr_client.batch(batch, force=True)