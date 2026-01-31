using Microsoft.Extensions.Localization;
using MokebyarCore.Localization;
using Volo.Abp.DependencyInjection;
using Volo.Abp.Ui.Branding;

namespace MokebyarCore;

[Dependency(ReplaceServices = true)]
public class MokebyarCoreBrandingProvider : DefaultBrandingProvider
{
    private IStringLocalizer<MokebyarCoreResource> _localizer;

    public MokebyarCoreBrandingProvider(IStringLocalizer<MokebyarCoreResource> localizer)
    {
        _localizer = localizer;
    }

    public override string AppName => _localizer["AppName"];
}
