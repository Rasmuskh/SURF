import tango

dev_info = tango.DbDevInfo()
dev_info.server = "OceanOptics/test"
dev_info._class = "OceanOptics"
dev_info.name = "test/ocean_optics/1"

db = tango.Database()
db.add_device(dev_info)

