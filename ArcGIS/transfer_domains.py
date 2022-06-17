import arcpy
from os import path


def transfer_domains(in_workspace, apply_workspace, domains=None):
    """
    Transfers list of domains using Domain to Table. If no list is given, all domains are transferred
    """

    if domains is None:
        domains = arcpy.da.ListDomains(in_workspace)

    for d in domains:
        domain_table = path.join(apply_workspace, d)

        arcpy.management.DomainToTable(
            in_workspace,
            domain_name=d,
            out_table=domain_table,
            code_field='code',
            description_field='description'
        )

        arcpy.management.TableToDomain(
            in_table=domain_table,
            in_workspace=apply_workspace,
            domain_name=d,
            code_field='code',
            description_field='description'
        )

        arcpy.Delete_management(domain_table)