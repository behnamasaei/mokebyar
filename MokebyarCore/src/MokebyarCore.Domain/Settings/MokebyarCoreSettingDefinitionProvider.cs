using Volo.Abp.Settings;

namespace MokebyarCore.Settings;

public class MokebyarCoreSettingDefinitionProvider : SettingDefinitionProvider
{
    public override void Define(ISettingDefinitionContext context)
    {
        //Define your own settings here. Example:
        //context.Add(new SettingDefinition(MokebyarCoreSettings.MySetting1));
    }
}
