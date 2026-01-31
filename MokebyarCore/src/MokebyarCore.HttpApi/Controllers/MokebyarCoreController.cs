using MokebyarCore.Localization;
using Volo.Abp.AspNetCore.Mvc;

namespace MokebyarCore.Controllers;

/* Inherit your controllers from this class.
 */
public abstract class MokebyarCoreController : AbpControllerBase
{
    protected MokebyarCoreController()
    {
        LocalizationResource = typeof(MokebyarCoreResource);
    }
}
