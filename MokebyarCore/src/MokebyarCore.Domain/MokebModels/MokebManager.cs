using System;
using System.Collections;
using System.Collections.Generic;
using Volo.Abp.Domain.Entities.Auditing;
using Volo.Abp.MultiTenancy;

namespace MokebyarCore.MokebModels;

public class MokebManager : FullAuditedAggregateRoot<Guid>, IMultiTenant
{
    public Guid? TenantId { get; }

    // شماره ثبتی
    public string? Code { get; set; }
    public required string ManagerName { get; set; }
    public required string ManagerPhone { get; set; }
    public required string Address { get; set; }
    public required string Location { get; set; }
    public ICollection<Mokeb>? Mokebs { get; set; }
}