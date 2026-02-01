using System;
using System.IO;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.Configuration;

namespace MokebyarCore.EntityFrameworkCore;

/* This class is needed for EF Core console commands
 * (like Add-Migration and Update-Database commands) */
public class MokebyarCoreDbContextFactory : IDesignTimeDbContextFactory<MokebyarCoreDbContext>
{
    public MokebyarCoreDbContext CreateDbContext(string[] args)
    {
        var configuration = BuildConfiguration();
        
        MokebyarCoreEfCoreEntityExtensionMappings.Configure();

        var builder = new DbContextOptionsBuilder<MokebyarCoreDbContext>()
            .UseNpgsql(configuration.GetConnectionString("Default"));
        
        return new MokebyarCoreDbContext(builder.Options);
    }

    private static IConfigurationRoot BuildConfiguration()
    {
        var builder = new ConfigurationBuilder()
            .SetBasePath(Path.Combine(Directory.GetCurrentDirectory(), "../MokebyarCore.DbMigrator/"))
            .AddJsonFile("appsettings.json", optional: false)
            .AddEnvironmentVariables();

        return builder.Build();
    }
}
