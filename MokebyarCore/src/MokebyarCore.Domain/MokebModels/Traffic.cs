using System;
using Volo.Abp.MultiTenancy;

namespace MokebyarCore.MokebModels;

public class Traffic : IMultiTenant
{
    public Guid? TenantId { get; }
    
    public Guid MokebId { get; set; }
    public Guid ReservationId { get; set; }
    public Guid PilgrimId { get; set; }
    public DateTime Time { get; set; }

    public virtual Mokeb? Mokeb { get; set; }
    public virtual Pilgrim? Pilgrim { get; set; }
    public virtual Reservation? Reservation { get; set; }
}