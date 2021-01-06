from zepben.evolve import GeographicalRegion, SubGeographicalRegion, PowerTransformer, Feeder, Breaker, Substation


region = GeographicalRegion()
sub_region = SubGeographicalRegion(geographical_region=region)
region.add_sub_geographical_region(sub_region)

substation = Substation(sub_geographical_region=sub_region)

sub_tx = PowerTransformer()
sub_tx.add_container(substation)
substation.add_equipment(sub_tx)

feeder = Feeder(normal_energizing_substation=substation)

feeder_cb = Breaker()
feeder_cb.add_container(feeder)
feeder.add_equipment(feeder_cb)
