using System;
using System.Linq;
using System.Threading.Tasks;
using MokebyarCore.IdentityContracts;
using Volo.Abp.Application.Services;
using Volo.Abp.Authorization;
using Volo.Abp.Identity;
using Volo.Abp.Users;

namespace MokebyarCore.Identity;

public class IdentityService : ApplicationService
{
    private readonly ICurrentUser _currentUser;
    private readonly IdentityUserManager _userManager;

    public IdentityService(
        ICurrentUser currentUser,
        IdentityUserManager userManager)
    {
        _currentUser = currentUser;
        _userManager = userManager;
    }

    public async Task<CurrentUserDto> GetCurrentUserAsync()
    {
        if (!_currentUser.IsAuthenticated)
            throw new AbpAuthorizationException("User is not authenticated");

        var user = await _userManager.GetByIdAsync(_currentUser.GetId());

        var roles = await _userManager.GetRolesAsync(user);
        var claims = await _userManager.GetClaimsAsync(user);

        return new CurrentUserDto
        {
            Id = user.Id,
            UserName = user.UserName,
            Email = user.Email,
            Name = user.Name,
            Surname = user.Surname,
            PhoneNumber = user.PhoneNumber,
            IsActive = user.IsActive,
            EmailConfirmed = user.EmailConfirmed,
            PhoneNumberConfirmed = user.PhoneNumberConfirmed,
            CreationTime = user.CreationTime,

            Roles = roles.ToList(),
            Claims = claims.Select(c => new UserClaimDto
            {
                Type = c.Type,
                Value = c.Value
            }).ToList(),

            ExtraProperties = user.ExtraProperties
        };
    }
}