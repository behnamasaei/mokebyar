using System;
using System.Collections;
using System.Collections.Generic;
using MokebyarCore.MokebDomainShared;
using Volo.Abp;
using Volo.Abp.Domain.Entities.Auditing;
using Volo.Abp.MultiTenancy;

namespace MokebyarCore.MokebModels;

public class Mokeb : FullAuditedAggregateRoot<Guid>, IMultiTenant
{
    public Guid? TenantId { get; }
    
    public required string Name { get; set; }
    public required string Address { get; set; }
    public required string Location { get; set; }
    public required string Phone { get; set; }
    public required int Capacity { get; set; }
    public required Gender Gender { get; set; }
    public required Guid MokebManagerId { get; set; }
    public virtual MokebManager? MokebManager { get; set; }
    public virtual ICollection<Reservation>? Reservations{ get; set; }
    public virtual ICollection<Traffic>? Traffics{ get; set; }
    
}