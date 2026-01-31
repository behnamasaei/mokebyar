using MokebyarCore.Localization;
using Volo.Abp.Application.Services;

namespace MokebyarCore;

/* Inherit your application services from this class.
 */
public abstract class MokebyarCoreAppService : ApplicationService
{
    protected MokebyarCoreAppService()
    {
        LocalizationResource = typeof(MokebyarCoreResource);
    }
}
