using System;
using System.Collections.Generic;

namespace MokebyarCore.IdentityContracts;

public class CurrentUserDto
{
    public Guid Id { get; set; }

    public string UserName { get; set; }
    public string Email { get; set; }

    public string Name { get; set; }
    public string Surname { get; set; }

    public string PhoneNumber { get; set; }

    public bool IsActive { get; set; }
    public bool EmailConfirmed { get; set; }
    public bool PhoneNumberConfirmed { get; set; }

    public DateTime CreationTime { get; set; }

    public List<string> Roles { get; set; }

    public List<UserClaimDto> Claims { get; set; }

    public IDictionary<string, object> ExtraProperties { get; set; }
}