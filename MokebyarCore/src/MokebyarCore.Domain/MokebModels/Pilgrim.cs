using System;
using System.Collections;
using System.Collections.Generic;
using MokebyarCore.MokebDomainShared;
using Volo.Abp;
using Volo.Abp.Domain.Entities.Auditing;
using Volo.Abp.MultiTenancy;

namespace MokebyarCore.MokebModels;

public class Pilgrim : AuditedAggregateRoot<Guid>, IMultiTenant
{
    public Guid? TenantId { get; }

    public string? FirstName { get; set; }
    public string? LastName { get; set; }
    public string? PassportNumber { get; set; }
    public Gender? Gender { get; set; }
    public string? Address { get; set; }
    public string? Phone { get; set; }
    public string? Nationality { get; set; }
    public string? State { get; set; }
    public string? City { get; set; }
    public byte[]? ProfileBlob { get; set; }
    

    public virtual ICollection<Reservation>? Reservations { get; set; }
    public virtual ICollection<Traffic>? Traffics { get; set; }
}