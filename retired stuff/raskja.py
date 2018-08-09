import tango

dev_info = tango.DbDevInfo()
dev_info.server = "PowerSupply/test"
dev_info._class = "PowerSupply"
dev_info.name = "test/powersupply/1"

db = tango.Database()
db.add_device(dev_info)

