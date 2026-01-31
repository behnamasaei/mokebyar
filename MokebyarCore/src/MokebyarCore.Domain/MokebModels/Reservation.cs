using System;
using System.Collections;
using System.Collections.Generic;
using System.Runtime.InteropServices.JavaScript;
using Volo.Abp.Domain.Entities;
using Volo.Abp.Domain.Entities.Auditing;
using Volo.Abp.MultiTenancy;

namespace MokebyarCore.MokebModels;

public class Reservation: Entity<Guid>, IMultiTenant
{
    public Guid? TenantId { get; }
    public Guid PilgrimId { get; set; }
    public Guid MokebId { get; set; }
    public DateTime EnterDate { get; set; }
    public DateTime ExitDate { get; set; }
    public int? PositionNumber { get; set; }

    public virtual Pilgrim? Pilgrim { get; set; }
    public virtual Mokeb? Mokeb{ get; set; }
    public virtual ICollection<Traffic>? Traffics { get; set; }
}